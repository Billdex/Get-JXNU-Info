import pymysql

# 连接数据库函数
def conn_db():
    conn = pymysql.connect(
        host='localhost',
        user='数据库用户名',
        passwd='数据库密码',
        db='数据库名称',
        charset='utf8')
    cur = conn.cursor()
    return conn, cur

# 更新语句，可执行update,insert语句
def exe_update(cur, sql):
    sta = cur.execute(sql)
    return sta

# 删除语句，可批量删除
def exe_delete(cur, ids):
    for eachID in ids.split(' '):
        sta = cur.execute('delete from cms where id =%d' % int(eachID))
    return sta

# 查询语句
def exe_query(cur, sql):
    cur.execute(sql)
    return cur

# 执行commit操作，插入语句才能生效
def exe_commit(cur):
    cur.connection.commit()

 # 关闭所有连接
def conn_close(conn, cur):
    cur.close()
    conn.close()