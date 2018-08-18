import pymysql


def get_columns(ip, user, password, db, table):
    db = pymysql.connect(ip, user, password, db)
    cursor = db.cursor()
    cursor.execute("show  columns from " + table)
    list = []
    results = cursor.fetchall()
    results = str(results).split('),')
    for i, r in enumerate(results):
        list.append(getCom(r))
    db.close()
    return list


def getCom(str):
    i = str.index("('")
    j = str.index(",")
    return str[i + 2:j - 1]
