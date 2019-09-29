import pymysql
from comment import Comment


# 数据库相关配置
host = "localhost"
user = "cbuser"
passwd = "cbpass"
database = "cookbook"
comment_tablename = "BilibiliGaomu"


# 连接到数据库
def connect_db():
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        charset='utf8mb4',
        database=database)

    c = conn.cursor()
    return conn, c


# 创建新表
def create_table(c):
    sql = "CREATE TABLE " + comment_tablename +\
          """(mid INT,
              username VARCHAR(50),
              rpid BIGINT,
              gender VARCHAR(4),
              content VARCHAR(5000),
              ctime VARCHAR(30),
              likes INT,
              rcount INT)"""
    c.execute(sql)


# 往数据库中插入相应的Comment信息
def insert_comment(c, conn, comments):
    sql = "INSERT INTO " + comment_tablename + \
        "(mid, username, rpid, gender, content, ctime, likes, rcount) VALUES\
        (%s, %s, %s, %s, %s, %s, %s, %s)"
    c.executemany(sql, comments)
    conn.commit()


# 获得满足条件的表内数据
def get_all_by_condition(c, tablename, condition_name, condition):
    sql = "SELECT * FROM " + tablename + " WHERE " + \
          condition_name + " =" + condition
    c.execute(sql)
    return c.fetchall()


# 获取相应表内所有数据
def get_all(c, tablename):
    sql = "SELECT * FROM " + tablename
    c.execute(sql)
    return c.fetchall()


# 获取所有的Comments
def get_all_comments(c):
    sql = "SELECT mid, username, rpid, gender,\
           content, ctime, likes, rcount FROM " + \
        str(comment_tablename)
    c.execute(sql)
    return c.fetchall()


def get_comment_by_id(c, rpid):
    sql = "SELECT mid, username, rpid, gender,\
            content, ctime, likes, rcount FROM " + \
        str(comment_tablename) + ' WHERE rpid = %s'
    c.execute(sql, (rpid,))
    return c.fetchall()
