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

def fetchPage(stuid):
    '''返回unicode形式的页面源码'''

    url = "http://www.scupec.com:4489/jncx/jncx.asp?textxh="
    result = urllib2.urlopen(url + stuid, timeout = 10)
    return result.read().decode('gbk')



if __name__ == '__main__':
    print fetchPage("1043111063")

