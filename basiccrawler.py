# coding:utf-8
# basiccrawler.py

# ------------- Basic Crawler ----------
# Version   :   0.5
# Author    :   Derek
# Date      :   2015-01-08
# Language  :   Python 2.7
# -------------   Revision   -----------
# 2005-01-09 : v0.2     : Add Cookie Jar 
# 2015-01-09 : v0.3     : Add feature about customized http headers
# 2015-01-09 : v0.4     : Add feature about post data 
# 2015-01-09 : v0.5     : Add set_args() and _add_headers() Methods
# 2015-01-09 : v0.5.1   : Change the Initialization of self.__extract_re
# --------------------------------------

import urllib2, re
import cookielib

class BasicCrawler(object):
    # Initial Method
    def __init__(self, url = '', **kw):
        self.__url = url
        self.__extract_re = '.*?' # Default Regular Expression
        self.__headers = {}
        self.__data = None 
        
        # Set Default Headers
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
        self.__headers['User-Agent'] = user_agent
        # Set Ohter Arguments
        self.set_args(**kw)

        # Initialize cookie and openenr
        self.__cookie = cookielib.CookieJar()
        self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        urllib2.install_opener(self.__opener)
        
    # Get Page Content And Cookie
    def get_page_and_cookie(self):
        req = urllib2.Request(self.__url, self.__data, self.__headers)
        try:
            resp = urllib2.urlopen(req)
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print 'HTTP Error : %s' % e.code
            elif hasattr(e, 'reason'):
                print 'URL Error : %s' % e.reason
            else:
                print 'Unknown Error!'
        
        content = resp.read()  # Read One Page for Each Request
        return content, self.__cookie

    # Extract Content Through Regular Expression
    def extract_content(self, content, r_exp):
        self.__extract_re = r_exp # Set Regular Expression
        item_list = re.findall(self.__extract_re, content, re.S) 
        return item_list

    # Set Arguments
    def set_args(self, **kw):
        try:
            if kw.has_key('url'):
                self.__url = kw['url']
            if kw.has_key('headers'):
                for key in kw['headers'].keys():
                    self.__headers[key] = kw['headers'][key]
            if kw.has_key('data'):
                self.__data = ''
                self.__data += (kw['data']) 
            else:
                self.__data = None
        except KeyError:
            print 'KeyError!\n' 
