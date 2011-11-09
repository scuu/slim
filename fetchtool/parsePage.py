#! /usr/bin/env python
# coding=utf-8
'''
#=============================================================================
#     FileName: parsePage.py
#         Desc: parse抓取到的页面
#       Author: Alsotang
#        Email: alsotang@gmail.com
#     HomePage: http://tangzhan.li
#      Version: 0.0.1
#   LastChange: 2011-11-09 22:42:46
#      History:
#=============================================================================
'''
from BeautifulSoup import BeautifulSoup
import json

def parsePage(pagefile):
    '''输出python的list类型数据'''

    soup = BeautifulSoup(pagefile)
    table = soup.findAll('table')[-3]
    trs = table.findAll('tr')

    try:
        stuid = trs[1].contents[1].text
    except:
        #说明这个页面为空
        return False
    name = trs[1].contents[3].text
    sex = trs[1].contents[5].text

    time = []
    try:
        for i in xrange(1, 100, 7):
            high = trs[i].contents[9].text
            weight = trs[i + 1].contents[9].text
            grade = trs[i].contents[13].text
            time.append([grade, high, weight])
    except IndexError, e:
        pass
    data = [stuid, name, sex, time]
    return data



if __name__ == '__main__':
    import fetch
    data = fetch.fetchPage("0843031062")
    data = parsePage(data)
    for i in data:
        try:
            if i + ' ':
                print i
                continue
        except TypeError:
            pass
        for j in i:
            for k in j:
                print k
            
