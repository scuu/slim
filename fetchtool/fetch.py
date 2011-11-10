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
import logging

def fetchPage(stuid, datalist):
    '''返回unicode形式的页面源码'''

    url = "http://www.scupec.com:4489/jncx/jncx.asp?textxh="
    result = urllib2.urlopen(url + stuid, timeout = 5)
    data = parsePage.parsePage(result.read().decode('gbk'))
    if data != False:
        datalist.append(data)
    else:
        return False
    return True

def fetchCollege(stuid):
    datalist = [] #一个学院的数据放进一个列表里面
    ori_stuid = stuid[0: 7]
    datafile = open(ori_stuid + '.txt', 'w')

    error = 0
    try:
        for i in xrange(999):
            stuid = ori_stuid + "%03d" % i



    except FetchCollegeError:
        pass
    return datalist



class FetchCollegeError(Exception):
    pass

if __name__ == '__main__':
    print fetchCollege("1043111063")

