# coding=utf8
import MySQLdb

def readAllData():
    paras = []
    with open('allData.data') as f:
        for i in f:
            i = eval(i)
            para = [    i[0], #学号
                        '', #name 
                        '',
                        i[7] or '', #民族
                        i[1] or '', #college
                        i[2] or '', #major
                        i[6] or '', #idcard
                        i[4] or '', #from
                        i[5] or '', #address
                        i[3] or '', #phone
                   ]
            paras.append(para)
    return paras

if __name__ == '__main__':
    conn = MySQLdb.connect(unix_socket="/opt/lampp/var/mysql/mysql.sock", user = 'root', passwd = 'woyewangle', \
                           db = 'scuu', charset = 'utf8')

    cursor = conn.cursor()

    sql = "INSERT INTO personal_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    paras = readAllData()
    cursor.executemany(sql,paras)
    conn.commit()
    cursor.close()
    conn.close()


