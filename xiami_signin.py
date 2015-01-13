# coding:utf-8
# xiamilogin.py

# ----------------- Xiami Login ---------------
# Version       :   0.1
# Author        :   Derek
# Date          :   2015-01-08
# Language      :   Python 2.7
# Revision      :   None

import urllib2, re, urllib
from basiccrawler import BasicCrawler

class XiamiLogin(BasicCrawler):
    # Inital Method
    def __init__(self, url = '', **kw):
        BasicCrawler.__init__(self, url, **kw)
    
    # Login Xiami Account And Go To Index Page
    def login_and_goto_index(self):
        # Login
        content, cookie = self.get_page_and_cookie()

        # Go to Index Page
        url = 'http://www.xiami.com/web'
        headers = { 'Referer'   : 'http://www.xiami.com/profile'}
        self.set_args(url=url, headers=headers)
        content, cookie = self.get_page_and_cookie()
        
        # Estimate Whether Logining Succeed
        r_exp = r'<div\s*class="icon">\s*<p>(.*?)[</p>$]'
        item_list = self.extract_content(content,r_exp)

        for item in item_list:
            if cmp('冥王之殇：'.decode('GBK'), item.decode('utf-8')) == 0:
                print 'Loging Success!'
                login_success = True
            else:
                print 'Login Fail!'
                login_success = False

        return login_success,content
        
    # Sign In
    def sign_in(self, index_html):
        # Find the sign in url and content.
        # If <a> tag doesn't contain '每日签到', exit
        r_exp = r'<div\s*class="idh"><a\s*class="check_in"\shref="(.*?)">(.*?)</a></div>'
        item_list = self.extract_content(index_html, r_exp)
        content = ''
        if len(item_list) != 0 and cmp('每日签到'.decode('GBK'), item_list[1].decode('utf-8')) == 0:
            check_in_url = 'http://www.xiami.com' + item_list[0]
            # print check_in_url
                
            check_in_headers = { 'Referer'   : 'http://www.xiami.com/web'}
            self.set_args(url=check_in_url, headers=check_in_headers)
            content, cookie = self.get_page_and_cookie()
            # Check if sign in succeed
            r_exp = r'<div\s*class="idh">已连续签到(\d+)天</div>'
            login_days = self.extract_content(content, r_exp)
            if item_list:
                print 'You have checked in ' + login_days + ' days!'
            else:
                print 'Sign in fail!'
        else:
            print 'It\'s not time to sign in again!'


# Execute
login_url = 'http://www.xiami.com/web/login'
login_headers = { 'Referer'   : 'http://www.xiami.com/web/login'
        } 
username = '373850089@qq.com'
pw = '220991029'
data_dict = {'email'        :   username,
             'password'     :   pw,
             'LoginButton'  :   '%E7%99%BB%E5%BD%95'
             }
login_data= urllib.urlencode(data_dict)
login_data = login_data.encode('utf-8')
xmLog = XiamiLogin(login_url, headers=login_headers, data=login_data)

# Login
login_success, index_html = xmLog.login_and_goto_index()

# Login Success, and sign in!
if login_success:
    xmLog.sign_in(index_html)

