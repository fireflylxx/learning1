# sys用于输入文件，re 正则化表达式用于处理文件转成列表
# time 用于显示程序运行时间 logging 在输入界面显示有无错误
import logging
import sys
import re
import time

# 定义
STACK = []
KEY_COUNT = 0
CASE_COUNT = [0]
SWITCH_COUNT = 0
IF_ELSE_COUNT = 0
IF_ELIF_ELSE_COUNT = 0

# 设定关键词元组字典，便于查找匹配
KEYWORDS = (
    "unsigned", "void", "volatile", "while",
    "struct", "switch", "typedef", "union",
    "short", "signed", "sizeof", "static",
    "const", "continue", "default", "do",
    "int", "long", "register", "return",
    "double", "else", "enum", "extern",
    "auto", "break", "case", "char",
    "float", "for", "goto", "if"
)


# 对文本进行处理，导入re，筛
def remake(path):
    data = open(path, mode='r').read()
    data_final = re.sub(r"\/\*([^\*^\/]*|[\**\/*]*|[^\**\/]*)*\*\/", "", data)  # 剔除注释块
    data_final = re.sub(r"\/\/[^\n]*", "", data_final)                          # 剔除注释行
    data_final = re.sub(r"\"(.*)\"", "", data_final)                            # 剔除字符串

    data_final = re.sub(r"[ \t\v\r\f]+", " ", data_final)                       # 剔除多余空格
    data_final = re.sub(r"[\n]+", "  ", data_final)                             # 分号变为双空格
    data_final = re.split(r"\W", data_final)                                    # 转成列表
    return data_final


def find_keywords(data_final):
    global STACK, KEY_COUNT  # 全局变量声明
    global CASE_COUNT, SWITCH_COUNT
    global IF_ELSE_COUNT
    global IF_ELIF_ELSE_COUNT

    data_iter = iter(range(len(data_final)))                  # 生成一个可迭代对象
    for i in data_iter:  # 和字典匹配查找
        temp = data_final[i]
        if temp != '' and temp in KEYWORDS:  # GRADE 1
            KEY_COUNT += 1

            if temp == "switch":  # GRADE 2
                SWITCH_COUNT += 1
                if CASE_COUNT[0] != 0:
                    CASE_COUNT.append(0)

            elif temp == "case":
                CASE_COUNT[-1] += 1

            elif temp == "if":  # GRADE 3 and GRADE 4
                STACK.append("if")

            elif temp == "else":
                if data_final[i + 1] == "if":
                    STACK.append('elif')
                    KEY_COUNT += 1
                    data_iter.__next__()

                else:
                    elif_flag = False
                    while STACK[-1] == "elif":
                        elif_flag = True
                        STACK.pop()
                    STACK.pop()

                    if elif_flag:
                        IF_ELIF_ELSE_COUNT += 1
                    else:
                        IF_ELSE_COUNT += 1


# 输出对应等级函数
def out_put(str3):
    grade = int(str3)
    if grade >= 5:
        print("文件输入的等级不对")

    if (grade >= 1) and (grade < 5):                         # 输出增加的等级要求
        print("total num:", KEY_COUNT)

    if (grade >= 2) and (grade < 5):
        print("switch num:", SWITCH_COUNT)
        print("case num: ", end='')
        if SWITCH_COUNT > 0:
            print(*CASE_COUNT, sep=' ')

    if (grade >= 3) and (grade < 5):
        print("if-else num:", IF_ELSE_COUNT)

    if grade == 4:
        print("if-elseif-else num:", IF_ELIF_ELSE_COUNT)


def count_key(path, lever):
    list_word = remake(path)  # 列表化
    find_keywords(list_word)  # 处理
    out_put(lever)  # 输出


# 主函数
if __name__ == "__main__":
    t = time.time()

    if len(sys.argv) > 1:
        PATH = sys.argv[1]  # 传入文件路径
        str2 = sys.argv[2]
    else:
        PATH = r'D:\PycharmProjects\pythonProject\key.c'
        str2 = '4'

    try:
        count_key(PATH, str2)                                # 调用函数块，判断是否抛出异常
    except IOError:
        logging.warning("你输入的文件路径有误")
