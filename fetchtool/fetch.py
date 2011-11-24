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
#   LastChange: 2011-11-09 22:27:56
#      History:
#=============================================================================
'''
import urllib2
import parsePage
import socket
import threading
import time


class fetch(object):
    def __init__(self, proxy = False):
        self.collegeEmpty = 0
        self.pageEmpty = 0
        self.datalist = [] #装载抓取到的数据
        self.THREADLIMIT = 20
        if proxy == 'goagent':
            opener = urllib2.build_opener(urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'}))
            urllib2.install_opener(opener)
    def fetchPage(self, stuid):
        '''返回unicode形式的页面源码'''

        url = "http://www.scupec.com:4489/jncx/jncx.asp?textxh="
        while True:
            try:
                result = urllib2.urlopen(url + stuid, timeout = 5)
                data = parsePage.parsePage(result.read().decode('gbk'))
            except (urllib2.URLError, socket.timeout):
                print 'timeout'
                continue
            if data:
                time.sleep(2) #否则会多线程时打印错误
                self.datalist.append(data)
                self.pageEmpty = 0
                return data
            else:
                self.pageEmpty += 1
                return False

    def fetchCollege(self, ori_stuid):
        """输入任意一个该学院的学号即可抓取整个学院"""

        ori_stuid = ori_stuid[0: 7]
        try:
            for i in xrange(999):
                while threading.activeCount() > self.THREADLIMIT:
                    time.sleep(1)
                stuid = ori_stuid + "%03d" % i
                print '正在抓取', stuid
                t = threading.Thread(target = self.fetchPage, args = (stuid,))
                t.start()
                if self.pageEmpty > 10:
                    raise FetchCollegeError
        except FetchCollegeError:
            self.pageEmpty = 0
            return self.datalist #抓取完学院后返回datalist
        finally:
            print "抓取", ori_stuid, '学院完毕'

    def writeToFile(self, filename = '抓取数据'):
        with open(filename, 'w') as f:
            for i in self.datalist:
                print >> f, i #每个数据一行



class FetchCollegeError(Exception):
    pass

if __name__ == '__main__':
    fetchtool = fetch(proxy = 'goagent')
    fetchtool.fetchCollege("1043111000")
    while threading.activeCount() > 1:
        time.sleep(5)
    fetchtool.writeToFile('1043111.txt')
    

