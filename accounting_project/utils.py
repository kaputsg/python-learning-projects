from datetime import datetime


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


def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except:
        return False


def is_valid_month(month_text):
    try:
        datetime.strptime(month_text, "%Y-%m")
        return True
    except:
        return False