#! /usr/bin/env python
# coding=utf-8
'''
#=============================================================================
#     FileName: fetch.py
#         Desc: 抓取体测页面之用
#       Author: Alsotang
#        Email: alsotang@gmail.com
#     HomePage: http://tangzhan.li
#      Version: 0.0.1
#   LastChange: 2011-11-25 10:53:33
#      History:
#           2011-11-25 多线程抓取；并可以使用goagent代理；
#=============================================================================
'''
import urllib2
import parsePage
import socket
import threading
import time


class fetch(object):
    """抓取体测数据的类"""

    def __init__(self, proxy = False):
        """初始化一些错误计数器；判断是否需要代理"""

        self.pageEmpty = 0 #这些是用来计数哪些页面数据为空的。mEmpty那四个是因为不懂如何称呼学号的相关部分,所以用
        self.collegeEmpty = 0 #组织学号时候的变量名来命名。
        self.kEmpty = 0
        self.jEmpty = 0
        self.iEmpty = 0
        self.thisCollegeHasData = False

        self.currentCollege = '' #防止抓取上一学院时未完成的线程干扰当先抓取，而设置了此变量。
        self.datalist = [] #装载抓取到的数据
        self.THREADLIMIT = 30
        if proxy == 'goagent':
            opener = urllib2.build_opener(urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'}))
            urllib2.install_opener(opener)

    def reset(self):
        self.pageEmpty = self.collegeEmpty = self.kEmpty = self.jEmpty = self.iEmpty = 0

    def fetchPage(self, stuid):
        '''返回unicode形式的页面源码'''

        url = "http://www.scupec.com:4489/jncx/jncx.asp?textxh="
        for i in xrange(5): #如超时，最多循环抓取5次
            try:
                result = urllib2.urlopen(url + stuid, timeout = 5)
                data = parsePage.parsePage(result.read().decode('gbk'))
            except (urllib2.URLError, socket.timeout):
                print 'timeout', stuid
                continue
            if data:
                self.datalist.append(data)
                if stuid[0:7] == self.currentCollege:
                    self.thisCollegeHasData = True  #证明该学院有人
                    self.reset()
                return data
            else:
                if stuid[0:7] == self.currentCollege:
                    self.pageEmpty += 1
                return False

    def fetchCollege(self, ori_stuid):
        """输入任意一个该学院的学号即可抓取整个学院"""

        try:
            for i in xrange(1, 999): 
                while threading.activeCount() > self.THREADLIMIT:
                    time.sleep(1)
                stuid = ori_stuid + "%03d" % i
                print '正在抓取', stuid
                t = threading.Thread(target = self.fetchPage, args = (stuid,))
                t.start()
                if self.pageEmpty > 10:
                    raise FetchCollegeError
        except FetchCollegeError:
            if self.thisCollegeHasData: #由于无论如何都要引发FetchCollegeError，所以要判断是否另该学院为空
                self.thisCollegeHasData = False
            else:
                self.collegeEmpty += 1
            pass
        finally:
            print "抓取", ori_stuid, '学院完毕'
            print [i[0] for i in self.datalist[-20:]]
            print '条目数量为', len(self.datalist)

    def writeToFile(self, filename = 'data.txt'):
        with open(filename, 'w') as f:
            for i in self.datalist:
                print >> f, i #每个数据一行
        return True

    def fetchRange(self, rangee = ''): 
        """为了不与内置的range冲突所以改名为rangee, rangee的格式为10 or 1043 or 104311 or 1043111"""

        self.iEmpty = 0
        for i in xrange(len(rangee) >= 2 and int(rangee[0:2]) or 8,len(rangee) >= 2 and int(rangee[0:2]) + 1 or 11 ): #例如08,09,10
            self.jEmpty = 0
            for j in (range(len(rangee) >= 4 and int(rangee[2:4]) or 41, len(rangee) >= 4 and int(rangee[2:4]) + 1 or 50) + [55,]): #例如43,44,45; 硬编码了55
                self.kEmpty = 0
                for k in xrange(len(rangee) >= 6 and int(rangee[4:6]) or 1, len(rangee) >= 6 and int(rangee[4:6]) + 1 or 100): #例如03,04,05
                    self.collegeEmpty = 0
                    for college in xrange(len(rangee) >= 7 and int(rangee[6:7]) or 1, len(rangee) >= 7 and int(rangee[6:7]) + 1 or 10): #例如1, 2, 3, 4
                        self.pageEmpty = 0
                        self.currentCollege = collegeNumber = "%02d%02d%02d%01d" % (i, j, k, college)
                        self.fetchCollege(collegeNumber)
                        if self.collegeEmpty >= 2:
                            self.kEmpty += 1
                            break
                    if self.kEmpty >= 2:
                        self.jEmpty += 1
                        break
                if self.jEmpty >= 2:
                    self.iEmpty += 1
                    break
            if self.iEmpty >= 2:
                break
         

class FetchCollegeError(Exception):
    pass

class kError(Exception):
    pass

class jError(Exception):
    pass

class iError(Exception):
    pass

def main():
    rangee = raw_input("请输入要抓取的学号范围，\n如：10 or 1043 or 104311 or 1043111: ")
    fetchtool = fetch(proxy = '')
    fetchtool.fetchRange(rangee)

    while threading.activeCount() > 1:
        time.sleep(5)
    fetchtool.writeToFile(rangee + '.txt')
    
if __name__ == '__main__':
    main()
