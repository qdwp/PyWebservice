# coding=utf-8
import MySQLdb
import time

__author__ = 'Qi Dun Wei'


class MySQL:
    def __init__(self):
        self.conn = MySQLdb.Connection(
            host='qdm20800247.my3w.com',
            port=3306,
            user='qdm20800247',
            passwd='wait3344',
            db='qdm20800247_db',
            charset='utf8'
        )
        try:
            self.cursor = self.conn.cursor()
        except:
            print "Connect to MySql failed."

    def execute_non_query(self, query_str):
        row_count = 0
        try:
            self.cursor.execute(query_str)
            row_count = self.cursor.rowcount
            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        except Exception, ex:
            self.cursor.close()
            self.conn.rollback()
            self.conn.close()
        return row_count

    def execute_scalar(self, query_str):
        try:
            self.cursor.execute(query_str)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                result = row[0]
                return result
            return None
        except:
            return None

    # 写入数据库
    def insert_table(self, xh, xm, xy, bj, mv, mm, av):
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        sql = u"INSERT INTO student_info(userXH, userXM, userXY, " \
              u"userBJ, mobileVersion, mobileModel, apkVersion, loginTime)VALUES"
        sql += u" ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')" \
            .format(xh, xm, xy, bj, mv, mm, av,
                    time.strftime(ISOTIMEFORMAT, time.localtime()))
        row_count = self.execute_non_query(sql)
        return row_count
