# keyCount 编程作业

### 软工第一次编程作业

| 这个作业属于哪个课程 | [构建之法-2021秋-福州大学软件工程](https://bbs.csdn.net/forums/fzuSoftwareEngineering2021?category=0) |
| -------------------- | ------------------------------------------------------------ |
| 这个作业要求在哪里   | [2021秋软工实践第一次个人编程作业](https://bbs.csdn.net/topics/600574694) |
| 这个作业的目标       | 实现对c和c++文件的关键词提取                                 |
| 学号                 | 181700319                                                    |

 

## 代码仓库

[Github 仓库](https://github.com/fireflylxx/learning1)



# 目录

 

| PSP                                   | Personal Software Process Stages | 预估耗时 | 实际耗时 |
| ------------------------------------- | -------------------------------- | -------- | -------- |
| Planning                              | 计划                             | 120      | 180      |
| Estimate                              | 预估用时                         | 2200     | 2710     |
| Development                           | 开发                             | 1000     | 1050     |
| Analysis                              | 需求分析                         | 20       | 30       |
| Design Spec                           | 生成设计文档                     | 20       | 40       |
| Design Review                         | 设计复审                         | 60       | 50       |
| Coding Standard                       | 代码规范                         | 30       | 20       |
| Design                                | 设计                             | 50       | 70       |
| Coding                                | 编码                             | 300      | 500      |
| Code Review                           | 代码复审                         | 200      | 350      |
| Test                                  | 测试                             | 150      | 120      |
| Reporting                             | 报告                             | 80       | 60       |
| Test Report                           | 测试报告                         | 80       | 60       |
| Size Measurement                      | 计算工作量                       | 30       | 40       |
| Postmortem & Process improvement Plan | 事后总结并提出改进计划           | 60       | 40       |

##  解题思路

###  选择语言

其它班级已布置了作业，作业类型其实也差不多。我参考了他们的意见，他们大多是采用 python 写的，同时输入文件采用 sys 模块，处理时候有多种方式，我采用了 re 包进行处理。剩下时间花在查找和参考网上的资料使用这两个工具。

###  re 预处理

将注释和代码里的部分转义字符筛去。用双空格代替换行，用空格缩减多余空格。为 if else 匹配区分提供判断条件。

###  字典

字典是一个好东西，我只需要把文件内容多余的东西用 re 包过滤好，剩下的将每个元素列表化，就可以直接和我创建的关键词元组进行匹配查找。（元组内部元素设定好就不会被改变，防止后面操作误调整关键词元组）。

###  关键词匹配和 switch 判断

关键词直接查找，记录下来即可。switch 也继续类似，查找直到遇见下一个 switch 即可。

###  if else && if elif else 

这里模拟一个堆栈进行匹配判断，预处理之后达到的理想效果是 if else 判断，if 之后就是 else 就为 if else 若是有空格就为if elif else 了。这是最完美的设想，但是距离达到还有一定的差距，后来也向一些同学请教了这个问题。但是感觉依然有着 bug 存在。并且后期大部分时间花在了预处理使得这一块的匹配更加简单。

总结一下，希望写 c/c++ 的同学要注意格式！！！ 

## 流程图和截图

###  流程图




###  Github 提交截图



 

 

###  coverage picrure

 

###   耗时情况占比
 



##  代码块

###  主函数

```
# 主函数
if __name__ == "__main__":
    t = time.time()

    if len(sys.argv) > 1:
        PATH = sys.argv[1]                                                   # 传入文件路径
        str2 = sys.argv[2]
    else:
        PATH = r'D:\PycharmProjects\pythonProject\key.c'
        str2 = '4'

    try:
        count_key(PATH, str2)                                                # 调用函数块，判断是否抛出异常
    except IOError:
        logging.warning("你输入的文件路径有误")


```

###  调用模块

```
def count_key(path, lever):

    list_word = remake(path)  # 列表化
    find_keywords(list_word)  # 处理
    out_put(lever)            # 输出
```



###   输入和预处理

```python
# 对文本进行处理，导入re筛选替换
def remake(path):
    data = open(path, mode='r').read()
    data_final = re.sub(r"\/\*([^\*^\/]*|[\**\/*]*|[^\**\/]*)*\*\/", "", data)  # 剔除注释块
    data_final = re.sub(r"\/\/[^\n]*", "", data_final)                          # 剔除注释行
    data_final = re.sub(r"\"(.*)\"", "", data_final)                            # 剔除字符串

    data_final = re.sub(r"[ \r\f\t\v]+", " ", data_final)                       # 转换为单空格
    data_final = re.sub(r"[\n]+", "  ", data_final)                             # 换行变为双空格
    
    data_final = re.split(r"\W", data_final)                                    # 转成列表
    return data_final

```



###  提取信息

```python
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

```

###  输出

```python
# 输出对应等级函数
def out_put(str3):
    grade = int(str3)
    if grade >= 5:
        print("文件输入的等级不对")

    if (grade >= 1) and (grade < 5):                # 输出增加的等级要求
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


```



##  总结

 





