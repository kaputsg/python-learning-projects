#定义函数
def show_menu():
    print("----------计算器----------")
    print("1.加法")
    print("2.减法")
    print("3.乘法")
    print("4.除法")
    print("5.查看历史记录")
    print("6.退出")

def calculate(func,symbol):
    a = get_number("请输入第一个数字 ")
    if symbol == "/":
        while True:
            b = get_number("请输入第二个数字 ")
            if b == 0:
                print("0不可以作为除数,请重新输入")
            else:
                break
    else:
        b = get_number("请输入第二个数字 ")
    result = func(a,b)
    print("结果是： ",result)
    historyList.append(f"{a} {symbol} {b} = {result}")
    print("--------------------")
        
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
        for i in history:
            print(i)

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

def main():
    while True:
        show_menu()
        choice = input("请选择功能： ")
        if choice in operations:
            operation = operations[choice]
            func = operation["func"]
            symbol = operation["symbol"]
            calculate(func,symbol)
        elif choice == "5":
            show_history(historyList)
            print("--------------------")
        elif choice == "6":
            print ("谢谢您的使用")
            break
        else :
            print ("输入错误请重试")
    
main()