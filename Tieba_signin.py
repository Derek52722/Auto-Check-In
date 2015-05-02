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
        



def sign_in():
    tieba_like_url = "http://tieba.baidu.com/f/like/mylike"
    my_cookie = "BAIDUID=E4F26116B6C64B016B1CF3C9F4F6CB84:FG=1; BIDUPSID=E4F26116B6C64B016B1CF3C9F4F6CB84; BAIDU_WISE_UID=wapp_1430558531086_670; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; qh[360]=1; BDRCVFR[35mUMIIWOJm]=mk3SLVN4HKm; H_PS_PSSID=13371_1431_13464_13074_12868_13321_12692_13691_10562_12722_13761_13780_11684_13741_13086_8498; Hm_lvt_90056b3f84f90da57dc0f40150f005d5=1430558563,1430578513; Hm_lpvt_90056b3f84f90da57dc0f40150f005d5=1430578513; HOSUPPORT=1; HISTORY=963dd48ead497232508fcf577f27adc2495d1174889b749cb929c371e0919ef3c471b90dee686c1c9621f4a12933ffac9e0555f17a; BDUSS=XROZWIwSjhCa2VaMlNLYkJnUVdCMGxuNUZWTThoVkM3Zy1wfjBmeTJwcFljbXhWQVFBQUFBJCQAAAAAAAAAAAEAAAA~Tl0D2qTN9dau6eQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFjlRFVY5URVV; PTOKEN=f707e39127b69b344919addb53cf30f0; STOKEN=2364cf6ea5bffad8d36ae905c6f730f49dd27410f645f830845cf91a867e8426; SAVEUSERID=69921eecb7db713d7001fb6bb2d16079; USERNAMETYPE=1; UBI=fi_PncwhpxZ%7ETasTIT-0QyTN%7Emvv3XY1mk7tSnHje34fLlRG7t0sBkQUDfiWDOFPzInkkvu%7E9LmWFw7YTBbrxUA5pXzgnIosQUV8X7Qsp6wJOSfD04H1u5Fo6Gpobi6g-J4HzDTmfLyviuyM7rPmudFuSTQNB-DAY4YQhoMgQLqyISSj4XS3cwGnxAihPa8dcloKHiInLyCDtzMuWn%7E1DY0LL71V60JSAM7dw__"
    BDUSS = 'XROZWIwSjhCa2VaMlNLYkJnUVdCMGxuNUZWTThoVkM3Zy1wfjBmeTJwcFljbXhWQVFBQUFBJCQAAAAAAAAAAAEAAAA~Tl0D2qTN9dau6eQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFjlRFVY5URVV'
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
    message = sign_in()
    print message
