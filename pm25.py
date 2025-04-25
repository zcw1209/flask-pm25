import pandas as pd
import pymysql


def open_db():
    conn = None
    try:
        conn = pymysql.connect(
            host="127.0.0.1", port=3306, user="root", passwd="12345678", db="demo"
        )
    except Exception as e:
        print("資料庫開啟失敗", e)

    return conn


def get_pm25_data_from_mysql():
    conn = None
    columns, datas = None, None
    try:
        conn = open_db()
        cur = conn.cursor()
        # sqlstr = "select MAX(datacreationdate) from pm25;"
        # cur.execute(sqlstr)
        # last_time=cur.fetchall()[0]
        # print(last_time)
        sqlstr = "select * from pm25 where datacreationdate=(select MAX(datacreationdate) from pm25);"
        cur.execute(sqlstr)
        # 輸出資料表欄位
        print(cur.description)
        columns = [col[0] for col in cur.description]
        # 實際的資料
        datas = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return columns, datas


# 本地運行
if __name__ == "__main__":
    conn = open_db()
    print(conn)
    columns, datas = get_pm25_data_from_mysql()
    print(columns)
