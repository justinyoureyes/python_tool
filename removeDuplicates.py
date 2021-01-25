# We will use data structures and data analysis tools provided in Pandas library
import pandas as pd

# Import retail sales data from an Excel Workbook into a data frame
# path = '/Documents/analysis/python/examples/2015sales.xlsx'
path = 'OCR验证数据20201223025910.xlsx'
# xlsx = pd.ExcelFile(path)
df = pd.read_excel(path, sheet_name='个人项目', engine='openpyxl')

print(df.columns)
print(df['uniqueId'])
# print(df['uniqueId'].duplicated())
# Let's add a new boolean column to our dataframe that will identify a duplicated order line item (False=Not a duplicate; True=Duplicate)
df['is_duplicated'] = df.duplicated(['uniqueId'])

# We can sum on a boolean column to get a count of duplicate order line items
# df['is_duplicated'].sum()

# Get the records of duplicated, If you need non-dup just use False instead
df_dup = df.loc[df['is_duplicated'] == True]

# Finally let's save our cleaned up data to a csv file
df_dup.to_csv('dup.csv', encoding='utf-8')
