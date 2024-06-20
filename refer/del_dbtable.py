import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect
from sqlalchemy import text
import mariadb

# Define the MariaDB engine using MariaDB Connector/Python

def DelDbTable(del_db_name,del_db_tbstr):
    # print(del_db_name) 要刪的資料庫名稱
    # print(del_db_tbstr) 要刪的資料表名稱內含的關鍵字
    engine = create_engine(f"mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/{del_db_name}", pool_size=100, max_overflow=100) #一次可以刪多一點
    # engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:nineseve9173!@127.0.0.1:3306/stock")
    inspector = inspect(engine)
    schemas = inspector.get_schema_names()

    for schema in schemas:
    #  print("schema: %s" % schema)
        if schema == del_db_name:
            for table_name in inspector.get_table_names(schema=schema):
                # print("1:",table_name)
                connet = engine.connect() #連上engine
                if del_db_tbstr in table_name:
                    query = f"DROP TABLE {table_name}"
                    print("刪除的資料表:",table_name)
                    connet.execute(text(query)) # 將quiry從物件變字串用text() 要引用才可使用
                    # result = connet.execute(text(query)) # 將quiry從物件變字串用text() 要引用才可使用
                    # print(result)
        # connet.close()
    #  for table_name in inspector.get_table_names(schema=schema):
    #     print(table_name)
        #   for column in inspector.get_columns(table_name, schema=schema):
                # print("Column: %s" % column)

    # quit()


