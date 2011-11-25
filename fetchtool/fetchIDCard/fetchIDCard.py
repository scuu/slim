# coding=utf-8
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

class fetchIDCard(object):
    def loginAndGetPage(self, stuid = None, pwd = None):
        """模拟浏览器登录并返回页面数据"""

        br = mechanize.Browser()

        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)

        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; \
                          rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1.fc9 Firefox/3.0.1')]

        br.open('http://202.115.44.198/')

        br.select_form(nr = 0)
        br.form['txtUserName'] = stuid
        br.form['txtPassWord'] = pwd
        br.submit()

        br.open("http://202.115.44.198/Office/StudentConsole/StuInfo.aspx?Id=99&Name=%BB%F9%B1%BE%D0%C5%CF%A2")

        return br.response().read().decode('gbk')

    def parsePage(self, pageData):
        soup = BeautifulSoup(pageData)
        return soup.find(id = 'txtICN')

if __name__ == '__main__':
    fetchtool = fetchIDCard()
    pageData = fetchtool.loginAndGetPage('1043111063', '1043111063')
    print fetchtool.parsePage(pageData).get('value')

    
