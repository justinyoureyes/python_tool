import pandas as pd

# Import retail sales data from an Excel Workbook into a data frame
# path = '/Documents/analysis/python/examples/2015sales.xlsx'
path = 'xiagao.xlsx'
# xlsx = pd.ExcelFile(path)
df = pd.read_excel(path, sheet_name='Sheet1', engine='openpyxl')
print(type(df))
print(df.columns)
groups = df.groupby("对接清算")
dicts = dict(list(groups))
for key, data in dicts.items():
    sql = """update product set clearing_personnel="""
    print(key)
    sql = sql + "\'" + key + "\'" + " where product_code in ("
    print(data['项目编码'])
    product_codes = []
    for product_code in data['项目编码']:
        product_codes.append("\'" + str(product_code) + "\'")
    product_codes_str = ",".join(product_codes)
    sql = sql + product_codes_str + ")"
    sql_format = ""
    for i in range(0, len(sql), 100):
        sql_format += sql[i:i + 100] + "\r\n"

    print(sql)
    # print(sql_format)
    # flag = sql_format.replace("\r\n", "") == sql
    # print(flag)
