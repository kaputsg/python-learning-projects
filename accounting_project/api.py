from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import DatabaseManager
from utils import get_today_date, is_valid_date, is_valid_month

app = FastAPI()

db = DatabaseManager()

class RecordCreate(BaseModel):
    type: str
    amount: float
    category: str
    note: str = ""

class RecordUpdate(BaseModel):
    amount: float
    category: str
    note: str = ""


def record_to_dict(record):
    return {
        "id": record[0],
        "date": record[1],
        "type": record[2],
        "amount": record[3],
        "category": record[4],
        "note": record[5]
    }

def records_to_list(records):
    result = []

    for record in records:
        result.append(record_to_dict(record))

    return result

def none_to_zero(value):
    if value is None:
        return 0
    return value

def record_exists(record_id: int):
    result = db.fetch_one(
        "SELECT id FROM records WHERE id = ?",
        (record_id,)
    )

    return result is not None

@app.get("/")
def home():
    return {
        "message": "Personal Accounting System API is running"
    }

@app.get("/records")
def get_records():
    records = db.fetch_all(
        "SELECT id, date, type, amount, category, note FROM records ORDER BY id"
    )

    return {
        "records": records_to_list(records)
    }

@app.post("/records")
def create_record(record: RecordCreate):
    if record.type not in ["收入", "支出"]:
        raise HTTPException(status_code=400, detail="type 只能是 收入 或 支出")

    if record.amount <= 0:
        raise HTTPException(status_code=400, detail="金额必须大于0")

    record_date = get_today_date()

    new_id = db.insert_record(
        "INSERT INTO records (type, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
        (record.type, record.amount, record.category, record.note, record_date)
    )

    return {
        "message": "记录添加成功",
        "record": {
            "id": new_id,
            "type": record.type,
            "amount": record.amount,
            "category": record.category,
            "note": record.note,
            "date": record_date
        }
    }

@app.put("/records/{record_id}")
def update_record(record_id: int, record: RecordUpdate):
    if not record_exists(record_id):
        raise HTTPException(status_code=404, detail="记录不存在")

    if record.amount <= 0:
        raise HTTPException(status_code=400, detail="金额必须大于0")

    db.execute_sql(
        "UPDATE records SET amount = ?, category = ?, note = ? WHERE id = ?",
        (record.amount, record.category, record.note, record_id)
    )

    return {
        "message": "记录修改成功",
        "record": {
            "id": record_id,
            "amount": record.amount,
            "category": record.category,
            "note": record.note
        }
    }


@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    if not record_exists(record_id):
        raise HTTPException(status_code=404, detail="记录不存在")

    db.execute_sql(
        "DELETE FROM records WHERE id = ?",
        (record_id,)
    )

    return {
        "message": "记录删除成功",
        "deleted_id": record_id
    }

@app.get("/summary")
def get_summary():
    income_result = db.fetch_one(
        "SELECT SUM(amount) FROM records WHERE type = ?",
        ("收入",)
    )

    expense_result = db.fetch_one(
        "SELECT SUM(amount) FROM records WHERE type = ?",
        ("支出",)
    )

    income_total = none_to_zero(income_result[0])
    expense_total = none_to_zero(expense_result[0])
    balance = income_total - expense_total

    return {
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": balance
    }

@app.get("/summary/month")
def get_month_summary(month: str):
    if not is_valid_month(month):
        raise HTTPException(status_code=400, detail="月份格式错误，请使用 YYYY-MM 格式")

    month_pattern = month + "%"

    income_result = db.fetch_one(
        "SELECT SUM(amount) FROM records WHERE type = ? AND date LIKE ?",
        ("收入", month_pattern)
    )

    expense_result = db.fetch_one(
        "SELECT SUM(amount) FROM records WHERE type = ? AND date LIKE ?",
        ("支出", month_pattern)
    )

    income_total = none_to_zero(income_result[0])
    expense_total = none_to_zero(expense_result[0])
    balance = income_total - expense_total

    return {
        "month": month,
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": balance
    }

@app.get("/summary/expense-by-category")
def get_expense_by_category():
    results = db.fetch_all(
        """
        SELECT category, SUM(amount)
        FROM records
        WHERE type = ?
        GROUP BY category
        ORDER BY SUM(amount) DESC
        """,
        ("支出",)
    )

    data = []

    for result in results:
        data.append({
            "category": result[0],
            "total_expense": result[1]
        })

    return {
        "expense_by_category": data
    }


@app.get("/records/search")
def search_records(keyword: str):
    keyword = keyword.strip()

    if keyword == "":
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")

    search_text = f"%{keyword}%"

    records = db.fetch_all(
        """
        SELECT id, date, type, amount, category, note
        FROM records
        WHERE type LIKE ? OR category LIKE ? OR note LIKE ?
        ORDER BY date, id
        """,
        (search_text, search_text, search_text)
    )

    return {
        "keyword": keyword,
        "records": records_to_list(records)
    }

@app.get("/records/by-date")
def get_records_by_date(record_date: str):
    if not is_valid_date(record_date):
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD 格式")

    records = db.fetch_all(
        """
        SELECT id, date, type, amount, category, note
        FROM records
        WHERE date = ?
        ORDER BY id
        """,
        (record_date,)
    )

    return {
        "date": record_date,
        "records": records_to_list(records)
    }

@app.get("/records/by-date-range")
def get_records_by_date_range(start_date: str, end_date: str):
    if not is_valid_date(start_date) or not is_valid_date(end_date):
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD 格式")

    if start_date > end_date:
        raise HTTPException(status_code=400, detail="开始日期不能晚于结束日期")

    records = db.fetch_all(
        """
        SELECT id, date, type, amount, category, note
        FROM records
        WHERE date BETWEEN ? AND ?
        ORDER BY date, id
        """,
        (start_date, end_date)
    )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "records": records_to_list(records)
    }

@app.get("/records/by-amount-range")
def get_records_by_amount_range(min_amount: float, max_amount: float):
    if min_amount < 0 or max_amount < 0:
        raise HTTPException(status_code=400, detail="金额不能小于0")

    if min_amount > max_amount:
        raise HTTPException(status_code=400, detail="最小金额不能大于最大金额")

    records = db.fetch_all(
        """
        SELECT id, date, type, amount, category, note
        FROM records
        WHERE amount BETWEEN ? AND ?
        ORDER BY amount, id
        """,
        (min_amount, max_amount)
    )

    return {
        "min_amount": min_amount,
        "max_amount": max_amount,
        "records": records_to_list(records)
    }
