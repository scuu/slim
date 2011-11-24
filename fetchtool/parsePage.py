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
    '''输出python的list类型数据的json表示'''

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
        for i in xrange(1, 10):
            grade = trs[i].contents[23].text
            high = trs[i].contents[7].text
            weight = trs[i].contents[9].text
            time.append([grade, high, weight])
    except IndexError, e:
        pass
    data = [stuid, name, sex, time]
    return data #返回json格式的数据



if __name__ == '__main__':
    import fetch
    fetchtool = fetch.fetch(proxy = "goagent")
    data = fetchtool.fetchPage("1043111008")
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
            
