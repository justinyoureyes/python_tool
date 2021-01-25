# coding=utf-8
# sqlserver的连接
import pyodbc
import pandas
import pymssql
import re
import urllib3
import sqlalchemy.types as tp
from sqlalchemy import create_engine


class MSSQL:
    def __init__(self, host, port, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port

    def GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};SERVER=10.10.2.120;DATABASE=Operation;UID=p-test-yxxj;PWD=Yntrust2020@18')
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        """
        cur = self.GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


def type_dict(df):  # 用来对csv中的数据进行类型选择，以对应mysql中的类型
    types_dict = {}
    for k, v in zip(df.columns, df.dtypes):
        if 'object' in str(v):
            types_dict.update({k: tp.VARCHAR(length=20)})
        if 'int' in str(v):
            types_dict.update({k: tp.INT()})
        if 'float' in str(v):
            types_dict.update({k: tp.Float})
        if 'date' in str(v):
            types_dict.update({k: tp.DATE})
    return types_dict


def main():
    # ms = MSSQL(host="10.10.2.120;", port="1433", user="p-test-yxxj", pwd="Yntrust2020@18",
    # db="Operation")
    # resList = ms.ExecQuery("SELECT top 100 * FROM LoanOcrCheckResult")
    # print(resList)
    path = 'loanOcrCheckResult.csv'
    # xlsx = pd.ExcelFile(path)
    df = pandas.read_csv(path, sep=',', error_bad_lines=False)
    # var = df.columns
    # print(var)
    # print(df.shape)
    # 处理表格中数据,自定义表头(中文为excel 中列名,英文为读取后为数据设置的列索引)

    # df.rename(columns={'ProductCode': 'ProductCode', 'ProductName': 'ProductName',
    #                    'UniqueId': 'UniqueId', 'LoanContractNumber': 'LoanContractNumber',
    #                    'PayStatus': 'PayStatus', 'PaymentTime': 'PaymentTime',
    #                    'Name': 'Name', 'CardNo': 'CardNo',
    #                    'OCRName': 'OCRName', 'OCRCardNo': 'OCRCardNo',
    #                    'OCRGender': 'OCRGender', 'OCRBirthday': 'OCRBirthday',
    #                    'OCRAddress': 'OCRAddress', 'OCRNation': 'OCRNation',
    #                    'OCRValidityStartTime': 'OCRValidityStartTime', 'OCRValidityEndTime': 'OCRValidityEndTime',
    #                    'OcrSwitch': 'OcrSwitch', 'OCRResult': 'OCRResult',
    #                    'OnfileStatus': 'OnfileStatus', 'CreateTime': 'CreateTime',
    #                    'ValidateTime': 'ValidateTime', 'OnfileTime': 'OnfileTime',
    #                    'CardFrontUploadId': 'CardFrontUploadId', 'CardReverseUploadId': 'CardReverseUploadId',
    #                    'OCRResultRemark': 'OCRResultRemark', 'MerId': 'MerId'}, inplace=True)
    print(df.columns)
    # for data in df.items():
    #     print(data)

    parametros = (
        # Driver que será utilizado na conexão
        'DRIVER={SQL Server};'
        # IP ou nome do servidor\Versão do SQL.
        'SERVER=10.10.2.120;'
        # Porta
        'PORT=1433;'
        # Banco que será utilizado.
        'DATABASE=Operation;'
        # Nome de usuário.
        'UID=p-test-yxxj;'
        # Senha.
        'PWD=Yntrust2020@18')

    # Convertendo a string para um padrão de URI HTML.
    from urllib import parse
    url_db = parse.quote_plus(parametros)
    engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % url_db, fast_executemany=True)
    datas = pandas.DataFrame(df)
    print(datas)
    datas.to_sql("LoanOcrCheckResult", con=engine, index=False, if_exists='append', dtype=type_dict(df))


if __name__ == '__main__':
    main()
