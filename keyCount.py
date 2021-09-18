# sys用于输入文件，re 正则化表达式用于处理文件转成列表
import sys
import re


# 定义变量
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
    data_final = re.sub(r"\/\*([^\*^\/]*|[\*^\/*]*|[^\**\/]*)*\*\/", "", data)               # 剔除注释块
    data_final = re.sub(r"[^\n]*", "", data_final)                              # 剔除注释行
    data_final = re.sub(r"\"(.*)\"", "", data_final)                            # 剔除字符串
    data_final = re.sub(r"[ \f\r\t\v]+", " ", data_final)                       # 剔除多余空格
    data_final = re.sub(r"[\n]+", "  ", data_final)                             # 替换换行为双空格
    data_final = re.sub(r"[{]+", "  ", data_final)                              # 替换大括号为双空格
    data_final = re.sub(r"[}]+", "  ", data_final)
    data_final = re.sub(r"[;]+", "  ", data_final)                              # 分号变为双空格
    data_final = re.split(r"\W", data_final)                                    # 转成列表
    return data_final


def find_keywords(data_final):
    global STACK, KEY_COUNT                                                     # 全局变量声明
    global CASE_COUNT, SWITCH_COUNT
    global IF_ELSE_COUNT
    global IF_ELIF_ELSE_COUNT

    data_iter = iter(range(len(data_final)))                                    # 生成一个可迭代对象
    for i in data_iter:                                                         # 和字典匹配查找
        temp = data_final[i]
        if temp != '' and temp in KEYWORDS:                                     # GRADE 1
            KEY_COUNT += 1

            if temp == "switch":                                                # GRADE 2
                SWITCH_COUNT += 1
                if CASE_COUNT[0] != 0:
                    CASE_COUNT.append(0)

            elif temp == "case":
                CASE_COUNT[-1] += 1

            elif temp == "if":                                                  # GRADE 3 and GRADE 4
                STACK.append("if")

            elif temp == "else":
                if data_final[i+1] == "if":
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
def out_put(grade):

    if grade >= 1:                                                     # python里无switch case 语句
        print("total num:", KEY_COUNT)

    if grade >= 2:
        print("switch num:", SWITCH_COUNT)
        print("case num:", end=' ')
        if SWITCH_COUNT > 0:
            print(*CASE_COUNT, sep=' ')

        else:
            print(0)

    if grade >= 3:
        print("if-else num:", IF_ELSE_COUNT)

    if grade >= 4:
        print("if-elseif-else num:", IF_ELIF_ELSE_COUNT)


# 主函数
if __name__ == "__main__":

    PATH = sys.argv[1]                                                        # 传入文件名
    str2 = sys.argv[2]                                                        # 传入等级并且转换类型
    GRADE = int(str2)
    FILE = remake(PATH)                                                       # 列表化
    find_keywords(FILE)                                                       # 处理
    out_put(GRADE)                                                            # 输出
