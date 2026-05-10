#定义函数
def show_menu():
    print("----------计算器V3----------")
    print("1.加法")
    print("2.减法")
    print("3.乘法")
    print("4.除法")
    print("5.查看历史记录")
    print("6.清空历史记录")
    print("7.查看最近一次计算")
    print("8.查看计算统计")
    print("9.退出")

def calculate(func,symbol,history,stats):
    a = get_number("请输入第一个数字 ")
    if symbol == "/":
        while True:
            b = get_number("请输入第二个数字 ")
            if b == 0:
                print("除数不能为0,请重新输入")
            else:
                break
    else:
        b = get_number("请输入第二个数字 ")
    result = func(a,b)
    print("结果是： ",result)
    history.append(f"{a} {symbol} {b} = {result}")
    stats[symbol] += 1
        
def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    return a/b

def show_history(history):
    if not history:
        print("没有历史记录")
    else :
        count = 1
        for i in history:
            print(f"{count}. {i}")
            count += 1

def clear_history(history,stats):
    if not history:
        print("没有历史记录可以清空")
    else:
        while True:
            choice = input("确认清空历史记录？ y/n\n")
            if choice == "y":
                history.clear()
                stats["+"] = 0
                stats["-"] = 0
                stats["*"] = 0
                stats["/"] = 0
                print("历史记录已成功清除")
                break
            elif choice == "n":
                print("已取消清空历史记录")
                return
            else:
                print("输入错误,请重新选择")

def show_latest_calculation(history):
    if not history:
        print("没有最近一次历史记录")
    else:
        print(f"最近一次计算： {history[-1]}")

def num_of_calculations(stats):
    print(f"加法次数： {stats['+']}")
    print(f"减法次数： {stats['-']}")
    print(f"乘法次数： {stats['*']}")
    print(f"除法次数： {stats['/']}")

def get_number(prompt):
    while True:
        text = input(prompt)
        try:
            number = float(text)
            return number
        except ValueError:
            print("请输入正确的数字 ")
            

#历史记录列表
historyList = []
#运算方式字典
operations = {
    "1": {"func": add, "symbol": "+"},
    "2": {"func": subtract, "symbol": "-"},
    "3": {"func": multiply, "symbol": "*"},
    "4": {"func": divide, "symbol": "/"}
}
#计算次数统计字典
stats = {
    "+": 0,
    "-": 0,
    "*": 0,
    "/": 0
}
def main():
    while True:
        show_menu()
        choice = input("请选择功能： ")
        if choice in operations:
            operation = operations[choice]
            func = operation["func"]
            symbol = operation["symbol"]
            calculate(func,symbol,historyList,stats)
            print("--------------------")
        elif choice == "5":
            show_history(historyList)
            print("--------------------")
        elif choice == "6":
            clear_history(historyList,stats)
            print("--------------------")
        elif choice == "7":
            show_latest_calculation(historyList)
            print("--------------------")
        elif choice == "8":
            num_of_calculations(stats)
            print("--------------------")
        elif choice == "9":
            print ("谢谢您的使用")
            break
        else :
            print ("输入错误请重试")
    
main()