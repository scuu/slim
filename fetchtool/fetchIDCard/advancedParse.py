# coding=utf-8
'''
#=============================================================================
#     FileName: tt.py
#         Desc: 从网页中得到[学院，专业，家长手机号（本来以为是该生手机号的），籍贯，家庭住址，身份证号，民族]等8项信息
#       Author: Alsotang
#        Email: alsotang@gmail.com
#     HomePage: http://tangzhan.li
#      Version: 0.0.1
#   LastChange: 2011-11-26 20:10:03
#      History:
#=============================================================================
'''
from BeautifulSoup import BeautifulSoup
import re

mobilePattern = re.compile(r'(^|\D)(1\d{10})($|\D)') #手机号的匹配规则。因为有时寝室寝室电话一栏会是:"07773674652-18607771234"的格式

def parsePage(pageData = None):
    dataList = [] #学号，学院，专业，家长手机号，籍贯，家庭地址，身份证号，民族
    if u'登录说明' in pageData: #如果是登录首页则退出
        return None
    soup = BeautifulSoup(pageData)

    dataList.append(soup.find(id = 'lblStuNo').text) #学号
    dataList.append(soup.find(id = 'lblCollegeName').text)
    dataList.append(soup.find(id = 'lblMajorName').text)
    try:
        dataList.append( #手机号码在‘手机’栏或者‘寝室电话’栏
            mobilePattern.search(
                    soup.find(id = 'txtMobile').get('value') or 
                    soup.find(id = 'txtPhone').get('value')
            ).group(2)
        )
    except:
        dataList.append('')
    dataList.append(soup.find(id = 'txtBaseFrom').get('value') or '')
    dataList.append(soup.find(id = 'txtHomeAddr').get('value') or '')
    #dataList.append(soup.findAll('input')[17].get('value') or '') #抓取家庭住址
    dataList.append(soup.find(id = 'txtICN').get('value') or '')
    dataList.append(soup.find(id = 'txtNation').get('value') or '')

    return dataList

def main():
    pass
    
if __name__ == '__main__':
    main()


