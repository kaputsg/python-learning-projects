from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = BASE_DIR / "records.json"

class AccountingSystem:
    def __init__(self):
        self.records = []

    def show_menu(self):
        print("====== 个人记账系统 V2 ======")
        print("1. 添加收入")
        print("2. 添加支出")
        print("3. 查看所有记录")
        print("4. 查看余额统计")
        print("5. 删除记录")
        print("6. 修改记录")
        print("7. 退出系统")

    def get_amount(self,prompt):
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

        record = {
            "type": record_type,
            "amount": amount,
            "category": category,
            "note": note
        }

        self.records.append(record)
        self.save_records()
        print(f"{record_type}记录添加成功")

    def save_records(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)
        print("数据保存成功")

    def load_records(self):
        global records

        if FILE_NAME.exists():
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                self.records = json.load(f)
            print("历史记录读取成功")
        else:
            self.records = []
            print("暂无历史记录")

    def show_records(self):
        if len(self.records) == 0:
            print("暂无记账记录")
        else:
            print("====== 所有记账记录 ======")
            for index, record in enumerate(self.records, start=1):
                print(f"{index}. 类型：{record['type']} | 金额：{record['amount']} | 分类：{record['category']} | 备注：{record['note']}")

    def show_summary(self):
        income_total = 0
        expense_total = 0

        for record in self.records:
            if record["type"] == "收入":
                income_total += record["amount"]
            elif record["type"] == "支出":
                expense_total += record["amount"]

        balance = income_total - expense_total

        print("总收入：", income_total)
        print("总支出：", expense_total)
        print("当前余额：", balance)

    def get_record_index(self, prompt):
        while True:
            user_input = input(prompt)

            if user_input == "q":
                return None

            try:
                index = int(user_input)

                if index < 1 or index > len(self.records):
                    print("编号不存在，请重新输入，或输入 q 返回菜单")
                else:
                    return index - 1

            except:
                print("请输入正确的编号，或输入 q 返回菜单")
    
    def delete_record(self):
        if len(self.records) == 0:
            print("暂无记录，无法删除")
            return

        self.show_records()

      
        index = self.get_record_index("请输入要删除的记录编号，输入 q 返回菜单：")

        if index is None:
            return

        confirm = input("确认删除这条记录吗？输入 y 确认，其他键取消：")

        if confirm == "y":
            deleted_record = self.records.pop(index)
            self.save_records()
            print(f"删除成功：类型：{deleted_record['type']} | 金额：{deleted_record['amount']} | 分类：{deleted_record['category']} | 备注：{deleted_record['note']}")
        else:
            print("已取消删除")

    def update_record(self):
        if len(self.records) == 0:
            print("暂无记录，无法修改")
            return

        self.show_records()

        index = self.get_record_index("请输入要修改的记录编号，输入 q 返回菜单：")

        if index is None:
            print("已取消修改")
            return

        record = self.records[index]

        print("当前记录：")
        print(f"类型：{record['type']} | 金额：{record['amount']} | 分类：{record['category']} | 备注：{record['note']}")

        amount = input("请输入新的金额，直接回车保持原金额：")

        if amount != "":
            try:
                amount = float(amount)
                if amount <= 0:
                    print("金额必须大于0，本次金额未修改")
                else:
                    record["amount"] = amount
            except:
                print("金额格式错误，本次金额未修改")

        category = input("请输入新的分类，直接回车保持原分类：")
        note = input("请输入新的备注，直接回车保持原备注：")

        if category != "":
            record["category"] = category

        if note != "":
            record["note"] = note

        self.save_records()
        print("记录修改完成")

    def run(self):
        self.load_records()

        while True:
            self.show_menu()
            choice = input("请输入您的选择 ")

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
                print("退出系统")
                break
            else:
                print("输入错误，请重新输入")

if __name__ == "__main__":
    system = AccountingSystem()
    system.run()