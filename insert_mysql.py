# -*- coding: utf-8 -*-
# sqlserver的连接
import pyodbc
import pandas
import sqlalchemy.types as tp
from sqlalchemy import create_engine
import sys

print(sys.getdefaultencoding())


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
            if len(k) > 1000:
                types_dict.update({k: tp.TEXT()})
            else:
                types_dict.update({k: tp.VARCHAR(length=20)})
        if 'int' in str(v):
            types_dict.update({k: tp.INT()})
        if 'float' in str(v):
            types_dict.update({k: tp.Float})
        if 'date' in str(v):
            types_dict.update({k: tp.DATE})
    return types_dict


def main():
    path = 'forum-mysql-dump.json'
    labels = ['category_id', 'comments', 'has_attach', 'id', 'message', 'title', 'uid', 'views', 'votes']
    df = pandas.read_json(path, lines=True)

    # Convertendo a string para um padrão de URI HTML.
    # from urllib import parse
    # url_db = parse.quote_plus(parametros)
    engine = create_engine('mysql://root:hzy110@localhost:3306/qa_es?charset=utf8mb4', encoding='utf-8', echo=True)
    datas = pandas.DataFrame(df)
    # print(datas)
    source = datas.get('_source')
    sdf = pandas.DataFrame({"info": source})
    tmp = sdf["info"].apply(pandas.Series)
    print(tmp)
    tmp.to_sql('aws_article', con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    main()
