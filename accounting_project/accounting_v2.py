from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = BASE_DIR / "records.json"

records = []

def show_menu():
    print("====== 个人记账系统 V1 ======")
    print("1. 添加收入")
    print("2. 添加支出")
    print("3. 查看所有记录")
    print("4. 查看余额统计")
    print("5. 删除记录")
    print("6. 修改记录")
    print("7. 退出系统")

def get_amount(prompt):
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

def save_records():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)
    print("数据保存成功")

def load_records():
    global records

    if FILE_NAME.exists():
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            records = json.load(f)
        print("历史记录读取成功")
    else:
        records = []
        print("暂无历史记录")

def add_income():
    amount = get_amount("请输入收入金额：")
    category = input("请输入收入分类：")
    note = input("请输入备注：")

    record = {
        "type": "收入",
        "amount": amount,
        "category": category,
        "note": note
    }

    records.append(record)
    print("收入记录添加成功")
    save_records()

def add_expense():
    amount = get_amount("请输入收入金额：")
    category = input("请输入支出分类：")
    note = input("请输入备注：")

    record = {
        "type": "支出",
        "amount": amount,
        "category": category,
        "note": note
    }

    records.append(record)
    print("支出记录添加成功")
    save_records()

def show_records():
    if len(records) == 0:
        print("暂无记账记录")
    else:
        print("====== 所有记账记录 ======")
        for index, record in enumerate(records, start=1):
            print(f"{index}. 类型：{record['type']} | 金额：{record['amount']} | 分类：{record['category']} | 备注：{record['note']}")

def show_summary():
    income_total = 0
    expense_total = 0

    for record in records:
        if record["type"] == "收入":
            income_total += record["amount"]
        elif record["type"] == "支出":
            expense_total += record["amount"]

    balance = income_total - expense_total

    print("总收入：", income_total)
    print("总支出：", expense_total)
    print("当前余额：", balance)

def delete_record():
    if len(records) == 0:
        print("暂无记录，无法删除")
        return

    show_records()

    try:
        index = int(input("请输入要删除的记录编号："))

        if index < 1 or index > len(records):
            print("编号不存在")
            return

        confirm = input("确认删除这条记录吗？输入 y 确认，其他键取消：")

        if confirm == "y":
            deleted_record = records.pop(index - 1)
            save_records()
            print(f"删除成功：类型：{deleted_record['type']} | 金额：{deleted_record['amount']} | 分类：{deleted_record['category']} | 备注：{deleted_record['note']}")
        else:
            print("已取消删除")

    except:
        print("请输入正确的编号")

def update_record():
    if len(records) == 0:
        print("暂无记录，无法修改")
        return

    show_records()

    try:
        index = int(input("请输入要修改的记录编号："))

        if index < 1 or index > len(records):
            print("编号不存在")
            return

        record = records[index - 1]

        print("当前记录：")
        print(f"类型：{record['type']} | 金额：{record['amount']} | 分类：{record['category']} | 备注：{record['note']}")

        amount = get_amount("请输入新的金额：")
        category = input("请输入新的分类：")
        note = input("请输入新的备注：")

        record["amount"] = amount
        record["category"] = category
        record["note"] = note

        save_records()
        print("记录修改成功")

    except:
        print("请输入正确的编号")

def main():
    while True:
        show_menu()
        choice = input("请输入您的选择 ")
        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            show_records()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            delete_record()
        elif choice == "6":
            update_record()
        elif choice == "7":
            print("退出系统")
            break
        else:
            print("输入错误，请重新输入")

load_records()
main()
