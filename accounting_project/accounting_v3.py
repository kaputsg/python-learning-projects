from pathlib import Path
import sqlite3
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "accounting.db"

class AccountingSystem:
    def __init__(self):
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                note TEXT
            )
        """)

        cursor.execute("PRAGMA table_info(records)")
        columns = cursor.fetchall()

        column_names = []
        for column in columns:
            column_names.append(column[1])

        if "date" not in column_names:
            cursor.execute("ALTER TABLE records ADD COLUMN date TEXT")
            
        cursor.execute("UPDATE records SET date = ? WHERE date IS NULL", ("未知日期",))

        conn.commit()
        conn.close()

    def show_menu(self):
        print("====== 个人记账系统 V3 数据库版 ======")
        print("1. 添加收入")
        print("2. 添加支出")
        print("3. 查看所有记录")
        print("4. 查看余额统计")
        print("5. 删除记录")
        print("6. 修改记录")
        print("7. 按日期查询记录")
        print("8. 按分类统计支出")
        print("9. 按日期范围查询记录")
        print("10. 按月份统计收支")
        print("11. 退出系统")

    def get_amount(self, prompt):
        while True:
            amount = input(prompt)
            try:
                amount = float(amount)
                if amount <= 0:
                    print("金额必须大于0")
                else:
                    return amount
            except:
                print("请输入正确的数字")

    def add_record(self, record_type):
        amount = self.get_amount(f"请输入{record_type}金额：")
        category = input(f"请输入{record_type}分类：")
        note = input("请输入备注：")
        record_date = datetime.now().strftime("%Y-%m-%d")

        self.execute_sql(
            "INSERT INTO records (type, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
            (record_type, amount, category, note, record_date)
        )

        print(f"{record_type}记录添加成功")

    def show_records(self):
        records = self.fetch_all(
            "SELECT id, date, type, amount, category, note FROM records ORDER BY id"
        )

        self.print_records(records, "====== 所有记账记录 ======")

    def show_summary(self):
        income_result = self.fetch_one(
            "SELECT SUM(amount) FROM records WHERE type = ?",
            ("收入",)
        )

        expense_result = self.fetch_one(
            "SELECT SUM(amount) FROM records WHERE type = ?",
            ("支出",)
        )

        income_total = income_result[0]
        expense_total = expense_result[0]

        if income_total is None:
            income_total = 0

        if expense_total is None:
            expense_total = 0

        balance = income_total - expense_total

        print("====== 余额统计 ======")
        print("总收入：", income_total)
        print("总支出：", expense_total)
        print("当前余额：", balance)

    def record_exists(self, record_id):
        result = self.fetch_one(
            "SELECT id FROM records WHERE id = ?",
            (record_id,)
        )

        return result is not None
    
    def count_records(self):
        result = self.fetch_one("SELECT COUNT(*) FROM records")
        return result[0]

    def delete_record(self):
        if self.count_records() == 0:
            print("暂无记录，无法删除")
            return

        self.show_records()

        while True:
            record_id = input("请输入要删除的记录 ID，输入 q 返回菜单：")

            if record_id == "q":
                print("已取消删除")
                return

            try:
                record_id = int(record_id)
            except:
                print("请输入正确的ID，或输入 q 返回菜单")
                continue

            if not self.record_exists(record_id):
                print("ID 不存在，请重新输入，或输入 q 返回菜单")
                continue

            break

        confirm = input("确认删除这条记录吗？输入 y 确认，其他键取消：")

        if confirm == "y":
            self.execute_sql(
                "DELETE FROM records WHERE id = ?",
                (record_id,)
            )
            print("删除成功")
        else:
            print("已取消删除")

    def get_record_by_id(self, record_id):
        return self.fetch_one(
            "SELECT id, date, type, amount, category, note FROM records WHERE id = ?",
            (record_id,)
        )
    

    def update_record(self):
        if self.count_records() == 0:
            print("暂无记录，无法修改")
            return

        self.show_records()

        while True:
            record_id = input("请输入要修改的记录 ID，输入 q 返回菜单：")

            if record_id == "q":
                print("已取消修改")
                return

            try:
                record_id = int(record_id)
            except:
                print("请输入正确的ID，或输入 q 返回菜单")
                continue

            record = self.get_record_by_id(record_id)

            if record is None:
                print("ID 不存在，请重新输入，或输入 q 返回菜单")
                continue

            break

        print("当前记录：")
        print(f"ID：{record[0]} | 日期：{record[1]} | 类型：{record[2]} | 金额：{record[3]} | 分类：{record[4]} | 备注：{record[5]}")

        amount = input("请输入新的金额，直接回车保持原金额：")

        if amount == "":
            new_amount = record[3]
        else:
            try:
                new_amount = float(amount)
                if new_amount <= 0:
                    print("金额必须大于0，本次金额保持原金额")
                    new_amount = record[3]
            except:
                print("金额格式错误，本次金额保持原金额")
                new_amount = record[3]

        category = input("请输入新的分类，直接回车保持原分类：")
        note = input("请输入新的备注，直接回车保持原备注：")

        if category == "":
            new_category = record[4]
        else:
            new_category = category

        if note == "":
            new_note = record[5]
        else:
            new_note = note

        self.execute_sql(
            "UPDATE records SET amount = ?, category = ?, note = ? WHERE id = ?",
            (new_amount, new_category, new_note, record_id)
        )

        print("记录修改成功")

    def show_records_by_date(self):
        record_date = input("请输入要查询的日期，格式为 YYYY-MM-DD：")

        try:
            datetime.strptime(record_date, "%Y-%m-%d")
        except:
            print("日期格式错误，请使用 YYYY-MM-DD 格式")
            return

        records = self.fetch_all(
            "SELECT id, date, type, amount, category, note FROM records WHERE date = ? ORDER BY id",
            (record_date,)
        )

        self.print_records(records, f"====== {record_date} 的记账记录 ======")

    def show_expense_by_category(self):
        results = self.fetch_all(
            """
            SELECT category, SUM(amount)
            FROM records
            WHERE type = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
            """,
            ("支出",)
        )

        if len(results) == 0:
            print("暂无支出记录")
        else:
            print("====== 按分类统计支出 ======")
            for result in results:
                print(f"分类：{result[0]} | 总支出：{result[1]}")

    def show_records_by_date_range(self):
        start_date = input("请输入开始日期，格式为 YYYY-MM-DD：")
        end_date = input("请输入结束日期，格式为 YYYY-MM-DD：")

        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except:
            print("日期格式错误，请使用 YYYY-MM-DD 格式")
            return

        if start_date > end_date:
            print("开始日期不能晚于结束日期")
            return

        records = self.fetch_all(
            """
            SELECT id, date, type, amount, category, note
            FROM records
            WHERE date BETWEEN ? AND ?
            ORDER BY date, id
            """,
            (start_date, end_date)
        )

        self.print_records(records, f"====== {start_date} 到 {end_date} 的记账记录 ======")

    def show_month_summary(self):
        month = input("请输入要统计的月份，格式为 YYYY-MM：")

        try:
            datetime.strptime(month, "%Y-%m")
        except:
            print("月份格式错误，请使用 YYYY-MM 格式")
            return

        month_pattern = month + "%"

        income_result = self.fetch_one(
            "SELECT SUM(amount) FROM records WHERE type = ? AND date LIKE ?",
            ("收入", month_pattern)
        )

        expense_result = self.fetch_one(
            "SELECT SUM(amount) FROM records WHERE type = ? AND date LIKE ?",
            ("支出", month_pattern)
        )

        income_total = income_result[0]
        expense_total = expense_result[0]

        if income_total is None:
            income_total = 0

        if expense_total is None:
            expense_total = 0

        balance = income_total - expense_total

        print(f"====== {month} 月度统计 ======")
        print("总收入：", income_total)
        print("总支出：", expense_total)
        print("本月余额：", balance)

    def print_records(self, records, title):
        if len(records) == 0:
            print("暂无记账记录")
        else:
            print(title)
            for record in records:
                print(f"ID：{record[0]} | 日期：{record[1]} | 类型：{record[2]} | 金额：{record[3]} | 分类：{record[4]} | 备注：{record[5]}")

    def execute_sql(self, sql, params=()):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(sql, params)

        conn.commit()
        conn.close()


    def fetch_all(self, sql, params=()):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(sql, params)
        results = cursor.fetchall()

        conn.close()

        return results


    def fetch_one(self, sql, params=()):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(sql, params)
        result = cursor.fetchone()

        conn.close()

        return result
    
    def run(self):
        while True:
            self.show_menu()
            choice = input("请输入您的选择：")

            if choice == "1":
                self.add_record("收入")
            elif choice == "2":
                self.add_record("支出")
            elif choice == "3":
                self.show_records()
            elif choice == "4":
                self.show_summary()
            elif choice == "5":
                self.delete_record()
            elif choice == "6":
                self.update_record()
            elif choice == "7":
                self.show_records_by_date()
            elif choice == "8":
                self.show_expense_by_category()
            elif choice == "9":
                self.show_records_by_date_range()
            elif choice == "10":
                self.show_month_summary()
            elif choice == "11":
                print("退出系统")
                break
            else:
                print("输入错误，请重新输入")

if __name__ == "__main__":
    system = AccountingSystem()
    system.run()