#定义函数
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
#历史记录列表
historyList = []
#菜单
while True:
    print("1.加法\n2.减法\n3.乘法\n4.除法\n5.查看历史记录\n6.退出")
    choice = input("请选择功能： ")
    if choice == "1":
        a = float(input("请输入第一个数字 "))#TODO 这里需要处理如果用户输入非数字该怎么处理
        b = float(input("请输入第二个数字 "))
        result = add(a,b)
        print("结果是： ",result)
        historyList.append(f"{a} + {b} = {result}")
        print("--------------------")
    elif choice == "2":
        a = float(input("请输入第一个数字 "))
        b = float(input("请输入第二个数字 "))
        result = subtract(a,b)
        print("结果是： ",result)
        historyList.append(f"{a} - {b} = {result}")
        print("--------------------")
    elif choice == "3":
        a = float(input("请输入第一个数字 "))
        b = float(input("请输入第二个数字 "))
        result = multiply(a,b)
        print("结果是： ",result)
        historyList.append(f"{a} * {b} = {result}")
        print("--------------------")
    elif choice == "4":
        a = float(input("请输入第一个数字 "))
        b = float(input("请输入第二个数字 "))
        if b == 0:
            print("除法不可以除以0")
        else :
            result = divide(a,b)
            print("结果是： ",result)
            historyList.append(f"{a} / {b} = {result}")
        print("--------------------")
    elif choice == "5":
        show_history(historyList)
        print("--------------------")
    elif choice == "6":
        print ("谢谢您的使用")
        break
    else :
        print ("输入错误请重试")
    
    