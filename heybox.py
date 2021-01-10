# -*- coding: UTF-8 -*-

"""

 * @author  cyb233

 * @date  2021/1/10 10:50

"""

import sys
import time
import requests
import re
import hashlib
from urllib.parse import urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
try:
    if len(sys.argv)==2 or len(sys.argv)==3:
        cookie = sys.argv[1]
    else:
        print("缺少必要参数！！！")
except Exception as e:
    print(e)

sign_path = 'https://api.xiaoheihe.cn/task/sign/'

def apiRequest_get(url,cookie,params):
    params_get = params
    headers_get = {
        'Cache-Control': 'Cache-Control:public,no-cache',
        'Referer': 'http://api.maxjia.com/',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/41.0.2272.118 Safari/537.36 ApiMaxJia/1.0',
        'Connection': 'Keep-Alive',
        'Host': 'api.xiaoheihe.cn',
        'Cookie': cookie
    }
    
    try:
        with requests.get(url, headers=headers_get, params=params_get, verify=False, timeout=300) as resp:
            res = resp.json()
            return res
    except Exception as ex:
        print(ex)

def gen_hkey(url: str,t:int) -> str:
    def url_to_path(url: str) -> str:
        path = urlparse(url).path
        if path and path[-1] == '/':
            path = path[:-1]
        return(path)
    def get_md5(data: str):
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        result = md5.hexdigest()
        return(result)
    h = f'{url_to_path(url)}/bfhdkud_time={t}'
    h = get_md5(h)
    h = h.replace('a', 'app')
    h = h.replace('0', 'app')
    h = get_md5(h)
    h = h[:10]
    return(h)
t=time.time()
hkey=gen_hkey(sign_path,t)
print('time: ',t)
print('hkey: ',hkey)
sign_time=str(int(t))

def mimikko(cookie):
    sign_data = apiRequest_get(sign_path + "?os_type=Android&version=1.3.135&hkey=" + hkey + "&_time=" + sign_time,cookie,"")
    if sign_data:
        if sign_data.get('status')=="ok":
            sign_result_post = '签到成功：' + sign_data['msg'] + str(sign_data)
        else:
            sign_result_post = '签到失败，今日已签到' + str(sign_data)
    else:
        sign_result_post = '签到请求失败' + str(sign_data)
    return sign_result_post

if cookie:
    sign_result_post = mimikko(cookie)
    print(sign_result_post)
    try:
        if len(sys.argv)==3:
            SCKEY = sys.argv[4]
            # print("有SCKEY")
            print("正在推送到微信")
            post_info = "?text=小黑盒每日签到&desp=<p>" + sign_result_post
            post_data = requests.get(server_api + SCKEY + '.send' + post_info)
            print(post_data)
        else:
            print("没有SCKEY")
    except Exception as e:
        print(e)
