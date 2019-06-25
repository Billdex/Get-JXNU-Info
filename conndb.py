import pymysql

# 连接数据库函数
def conn_db(host, user, password, db, charset='utf8'):
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=password,
        db=db,
        charset=charset)
    cur = conn.cursor()
    return conn, cur


# 删除语句，可批量删除
def exe_delete(cur, table, ids):
    for eachID in ids.split(' '):
        sta = cur.execute('delete from {} where id ={}'.format(table, int(eachID)))
    return sta

# 基础查询语句
def exe_query(cur, table, key, value, method='='):
    cur.execute('select * from {} where {} {} {}'.format(table, key, method, value))
    return cur

# 执行commit操作，插入语句才能生效
def exe_commit(cur):
    cur.connection.commit()

 # 关闭所有连接
def conn_close(conn, cur):
    cur.close()
    conn.close()