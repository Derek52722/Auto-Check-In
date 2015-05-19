# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: tiebasignin.py
#         Desc: 
#       Author: Derek Xu
#        Email: xuguang252@gmail.com

#      Version: 0.0.1
#   LastChange: 2015-05-02 16:39:02
#      History:
#=============================================================================
'''

from basiccrawler import BasicCrawler
import urllib2, re, urllib
import hashlib
import json

class TiebaSignin(BasicCrawler):
    # Initial Method
    def __init__(self, url='', **kw):
        BasicCrawler.__init__(self, url, **kw)

    # Login Baidu Tieba by Cookie and get liked list
    def get_liked_list(self):
        content, cookie = self.get_page_and_cookie()
        r_exp = r'<td>\s*<a\s*href="\/f\?kw=.*?"\s*title="(.*?)">.*?</a>\s*</td>'
        content = content.decode('gbk').encode('utf8')
        liked_list = self.extract_content(content, r_exp)
        return liked_list

    # Get fid, tbs
    def get_tieba_info(self, kw):
        tieba_wap_url = 'http://tieba.baidu.com/mo/m?kw='
        tieba_wap_url += kw
        self.set_args(url=tieba_wap_url)
        content, cookie = self.get_page_and_cookie()

        r_exp = r'<td\s*style="text-align:right;">\s*<span\s*>(.*?)</span>\s*</td>\s*</tr>'
        item_list = self.extract_content(content, r_exp)
        if len(item_list) != 0:
            is_sign_in = True

        else:
            is_sign_in = False

        re_fid = r'<input\s*type="hidden"\s*name="fid"\s*value="(.+?)"/>' 
        fid = self.extract_content(content, re_fid)[0] or None
        re_tbs = r'<input\s*type="hidden"\s*name="tbs"\s*value="(.+?)"\/>'
        tbs = self.extract_content(content, re_tbs)[0] or None
        
        return is_sign_in, fid, tbs
    
    def _decode_uri_post(self, postData):
        SIGN_KEY = "tiebaclient!!!"
        s = ""
        keys = postData.keys()
        keys.sort()
        for i in keys:
            s += i + '=' + postData[i]
        sign = hashlib.md5(s + SIGN_KEY).hexdigest().upper()
        postData.update({'sign': str(sign)})
        return postData
   
    # Get sign in data with fid, tbs and BDUSS
    def make_sign_in_data(self, kw, fid, tbs, BDUSS):
        sign_url = 'http://c.tieba.baidu.com/c/c/forum/sign'
        sign_data = {"BDUSS": BDUSS, "_client_id": "03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36", "_client_type": "4", "_client_version": "1.2.1.17", "_phone_imei": "540b43b59d21b7a4824e1fd31b08e9a6", "fid": fid, "kw": kw, "net_type": "3", 'tbs': tbs}

        sign_data = self._decode_uri_post(sign_data)
        sign_data = urllib.urlencode(sign_data)
        return sign_data
        



def sign_in(my_cookie, BDUSS):
    tieba_like_url = "http://tieba.baidu.com/f/like/mylike"
    login_headers = {'Cookie' : my_cookie, 'User-Agent': 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.1.16352'}

    tb = TiebaSignin()
    tb.set_args(url=tieba_like_url, headers=login_headers)
    liked_list = tb.get_liked_list()
    
    message = ''
    if len(liked_list) != 0:
        for item in liked_list:
            is_sign_in, fid, tbs = tb.get_tieba_info(item)
            if is_sign_in:
                message += item.decode('utf8') + ': It\'s not the time to sign in again!\n'
            else:
                sign_data = tb.make_sign_in_data(item, fid, tbs, BDUSS)
                sign_url = 'http://c.tieba.baidu.com/c/c/forum/sign'
                sign_header = {"Content-Type": "application/x-www-form-urlencoded"}
                tb.set_args(url=sign_url, data=sign_data, headers=sign_header)
                content, cookie = tb.get_page_and_cookie(timeout=5)
                content_dict = eval(content)
                error_code = content_dict['error_code']
                if error_code == '0':
                    message += item.decode('utf8') + ': Sign In Success!\n'
                else:
                    message += item.decode('utf8') + ': Sign In Fail!\n'


    else:
        message += 'Login Fail£¡'

    return message



if __name__ == "__main__":
    with open("tieba.json", "r") as f:
        my_info = json.load(f)
    message = sign_in(my_info['my_cookie'], my_info['BDUSS'])
    print message
