import pandas as pd
import re


def hump2underline(hump_str):
    """
    驼峰形式字符串转成下划线形式
    :param hump_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    """
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hump_str).lower()
    return sub


def json_hump2underline(hump_json_str):
    """
    把一个json字符串中的所有字段名都从驼峰形式替换成下划线形式。
    注意点：因为考虑到json可能具有多层嵌套的复杂结构，所以这里直接采用正则文本替换的方式进行处理，而不是采用把json转成字典再进行处理的方式
    :param hump_json_str: 字段名为驼峰形式的json字符串
    :return: 字段名为下划线形式的json字符串
    """
    # 从json字符串中匹配字段名的正则
    # 注：这里的字段名只考虑由英文字母、数字、下划线组成
    attr_ptn = re.compile(r'"\s*(\w+)\s*"\s*:')
    # 使用hump2underline函数作为re.sub函数第二个参数的回调函数
    sub = re.sub(attr_ptn, lambda x: '"' + hump2underline(x.group(1)) + '" :', hump_json_str)
    return sub


# Import retail sales data from an Excel Workbook into a data frame
# path = '/Documents/analysis/python/examples/2015sales.xlsx'
path = 'assetinfo.xlsx'
# xlsx = pd.ExcelFile(path)
df = pd.read_excel(path, sheet_name='Sheet1', engine='openpyxl')
# print(type(df))
# print(df)
# print(df.columns)
list = []
for item in df.itertuples():
    # print(item)
    if type(item.参数) == str and item.参数 is not None and item.参数 != 'nan':
        string = hump2underline(item.参数).upper() + "(" + "\"" + item.参数 + "\"" + "," + "\"" + item.注释.replace(" ",
                                                                                                              "") + "\"" + ")"
        list.append(string)
        # print(item.注释)
print(",\r\n".join(list))

jsonArray = []
for row in df.itertuples():
    if type(row.参数) == str and row.参数 is not None and row.参数 != 'nan':
        jsonRow = "\"" + row.参数 + "\"" + ":" + "\"" + "1" + "\""
        jsonArray.append(jsonRow)

print("{"+",".join(jsonArray)+"}")
