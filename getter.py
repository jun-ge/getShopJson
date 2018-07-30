import json
import random
import time
from urllib.parse import urlencode

import requests

from redisClient import RedisClient


class Getter:
    def __init__(self, key='男鞋'):
        self.base_url = 'https://pub.alimama.com/items/search.json?'
        self.conn = RedisClient()
        self.key = key

    def getCookie(self):
        s = requests.session()
        loginUrl = 'https://pub.alimama.com/'
        postData = {}
        rs = s.post(loginUrl, postData)
        c = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
        c.set('cookie-name', 'cookie-value')
        s.cookies.update(c)
        print(s.cookies.get_dict())

    def run(self):
        # jsonData = json.dumps([self.getJson(page) for page in range(1, 101)])
        jsonData = self.getJson(1)
        self.conn.add(jsonData)
        return jsonData

    def getJson(self, page):
        headers = {
            #'cookie':self.getCookie(),
            #'refer': 'https://pub.alimama.com/promo/search/index.htm?q=%E7%94%B7%E9%9E%8B&_t=1532934172077&toPage=1&perPageSize=50',
            'x-requested-with': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        t = int(time.time() * 1000)
        params = {
            'q': self.key,
            '_t': t - 120000,  # 用户登入时间戳
            'toPage': page,  # 页数
            'perPageSize': 50,  # 每页展示的数量
            'auctionTag': None,  # 作用未知
            'shopTag': 'yxjh',  # 作用未知
            't': t,  # 最近一次刷新时间戳.精确到毫秒
            '_tb_token_': 'f4ee47d336d34',  #
            # 'pvid': '10_115.190.248.241_515_1532935589260',  # 10 + ip + 随机数（num) +
            'pvid': '10_115.190.248.241_' + str(random.randint(100, 9999)) + '_' + str(t - 650)
        }
        url = self.base_url + urlencode(params)
        headers['cookie'] = 'log=lty=Ug%3D%3D; cookieCheck=80028; t=cd639e92749d725417e1dc7ffbf61197; cookie2=1f3d92c1bd0f28d7fb1cbb4acbe28bf5; v=0; _tb_token_=3be3add4080e7; cna=U/A4EwU2BSYCAdOhoOPCBeFZ; _umdata=70CF403AFFD707DFCBC0A061E697231DF2FA185F3EFA4FE20AF47EAD28EA0DB6A0D728BD03756153CD43AD3E795C914C22F3E2D702054476B4E0B40E27AB2B0C; unb=2849487666; lid=%E8%B4%AD%E4%B8%9Cgoudong; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=UIHiLt3xSard&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false&pas=0&cookie14=UoTfKf4e6sQEOw%3D%3D&tag=8&lng=zh_CN; sg=g6d; _l_g_=Ug%3D%3D; skt=e9444949cab6cd7a; lc=VynNk7l9pEmGCf4jjqxXFQ%3D%3D; cookie1=VyguQNX5qXZE3MdCEK3QrrKVkZUz5Q2XbyEaXQJSV7k%3D; csg=2f47c9ee; uc3=vt3=F8dBzrmR%2BJxohIzQWIU%3D&id2=UUBc8nM%2F1bcGiQ%3D%3D&nk2=2jUtnF6NttehK5M%3D&lg2=UtASsssmOIJ0bQ%3D%3D; existShop=MTUzMjk0NTY1Mg%3D%3D; tracknick=%5Cu8D2D%5Cu4E1Cgoudong; lgc=%5Cu8D2D%5Cu4E1Cgoudong; _cc_=UtASsssmfA%3D%3D; dnk=%5Cu8D2D%5Cu4E1Cgoudong; _nk_=%5Cu8D2D%5Cu4E1Cgoudong; cookie17=UUBc8nM%2F1bcGiQ%3D%3D; tg=0; mt=np=; isg=BICAfwOUzx1SKbMZTtfLYtl9UQ6SoW5vw_ays_oR5hsudSmfphk0Y1ZHi50QXhyr'
        try:
            re = requests.get(url, headers=headers)
            if re.status_code == 200:
                return json.dumps(re.json(), ensure_ascii=False)
        except TimeoutError:
            print('connect timeout')


if __name__ == '__main__':
    # print(time.time())
    print(Getter().run())
