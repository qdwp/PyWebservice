# coding=utf-8
import threading
import requests
import time
from library.mysql_db import MySQL

__author__ = 'qidunwei'


class MyThread(threading.Thread):
    def __init__(self, student, version, model, apk):
        threading.Thread.__init__(self)
        self.userXH = student.get('userXH')
        self.userXM = student.get('userXM')
        self.userXY = student.get('userXY')
        self.userBJ = student.get('userBJ')
        self.mobileVersion = version
        self.mobileModel = model
        self.apkVersion = apk

    def run(self):
        # ISOTIMEFORMAT = '%Y-%m-%d %X'
        # url = 'http://dunwei.top/ahutcourse/saveStudentInfo.php'
        # data = {
        #     'xh': self.userXH,
        #     'xm': self.userXM,
        #     'xy': self.userXY,
        #     'bj': self.userBJ,
        #     'mv': self.mobileVersion,
        #     'mm': self.mobileModel,
        #     'av': self.apkVersion,
        #     'tm': time.strftime(ISOTIMEFORMAT, time.localtime())
        # }
        # requests.post(url, data=data)
        mysql = MySQL()
        mysql.insert_table(self.userXH, self.userXM, self.userXY, self.userBJ, self.mobileVersion, self.mobileModel,
                           self.apkVersion)
