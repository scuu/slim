#! /usr/bin/env python
# coding=utf-8
'''
#=============================================================================
#     FileName: main.py
#         Desc: 获取对应学号的身份证号。
#       Author: Alsotang
#        Email: alsotang@gmail.com
#     HomePage: http://tangzhan.li
#      Version: 0.0.1
#   LastChange: 2011-11-26 00:07:46
#      History:
#=============================================================================
'''

from fetchIDCard import fetchIDCard
import threading
import time

IDCardList = []
THREADLIMIT = 30
fetchtool = fetchIDCard()

def threadCatch(stuid):
    pageData = fetchtool.loginAndGetPage(stuid, stuid)
    IDCard = fetchtool.parsePage(pageData)
    IDCardList.append(IDCard or '')
    print IDCard
    time.sleep(1)

def main():
    with open('stuidList.data') as f:
        stuidList = f.read().split('||') #所有已知的学号

    for i in stuidList:
        while threading.activeCount() > THREADLIMIT:
            time.sleep(1)
        t = threading.Thread(target = threadCatch, args = (i,))
        t.start()

if __name__ == '__main__':
    main()
