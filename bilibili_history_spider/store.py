import pymysql
import json
import re
import os

from Database import Database


def table_exists(con, table_name):  # 这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list or table_name.lower() in table_list:
        return True  # 存在返回1
    else:
        return False  # 不存在返回0


if __name__ == "__main__":
    database = Database()
    try:
        db = pymysql.connect(host=database.host, user=database.user, port=database.port, password=database.passwd,
                             database=database.name, charset=database.charset)
    except pymysql.err.OperationalError as oe:
        print("connect failed: ", oe)
        exit()

    cursor = db.cursor()
    if table_exists(cursor, "BILIBILI_HISTORY"):
        file_name = "new_data.json"
    else:
        file_name = "history.json"
        sql_create = """CREATE TABLE BILIBILI_HISTORY(
                TITLE       VARCHAR(200),
                UP_NAME     VARCHAR(20),
                VIDEO_TYPE  VARCHAR(30),
                DEVICE      CHAR(10),
                TIME        DATE
                )"""
        cursor.execute(sql_create)
    sql_change_charset = """ALTER TABLE BILIBILI_HISTORY CONVERT TO CHARACTER SET utf8mb4"""
    cursor.execute(sql_change_charset)
    with open(file_name, "r", encoding="utf-8") as fp:
        new_datas = json.load(fp)
    try:
        os.remove("new_data.json")
    except Exception:
        print()
    sql_add = """INSERT INTO BILIBILI_HISTORY(TITLE, UP_NAME, VIDEO_TYPE, DEVICE, TIME) VALUES (%s, %s,
                %s, %s, %s)"""

    for data in reversed(new_datas):
        try:
            var = (data.get("title"), data.get("up_name"), data.get("video_type"), data.get("device"), data.get("time"))
            cursor.execute(sql_add, var)
            db.commit()
        except pymysql.err.OperationalError as e:
            print(e)
            break
    db.close()
