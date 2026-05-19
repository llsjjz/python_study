
#if,elif,else
a = int(input("请输入一个整数："))

if a > 0:
    print("这是一个正数")
elif a < 0:
    print("这是一个负数")
else:
    print("这是零")

#match,case
b = int(input("请输入一个整数："))

match b:
    case 0|-0:
        print("这是零")
    case _:
        print("这不是零")