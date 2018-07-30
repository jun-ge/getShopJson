from urllib.parse import urlencode

import requests

from reidsClient import RedisClient


class Getter:
    def __init__(self, key='%E9%9E%8B%E5%AD%90'):
        # self.url = 'https://pub.alimama.com/promo/search/index.htm?q=%E7%94%B7%E9%9E%8B&_t=1532934172077&toPage=1&perPageSize=50'
        self.base_url = 'https://pub.alimama.com/items/search.json?'
        self.conn = RedisClient()

    def run(self):
        jsonData = self.getJson()
        self.conn.add(jsonData)
        return jsonData

    def getJson(self):
        headers = {
            'cookies': 'cna=U/A4EwU2BSYCAdOhoOPCBeFZ; t=005cc12495c7d60b46e0fc0b93d42480; account-path-guide-s1=true; 114246636_yxjh-filter-1=true; undefined_yxjh-filter-1=true; _umdata=70CF403AFFD707DFCBC0A061E697231DF2FA185F3EFA4FE20AF47EAD28EA0DB6A0D728BD03756153CD43AD3E795C914C22F3E2D702054476B4E0B40E27AB2B0C; cookie2=19dc8ac02a29f33886e13345d4b13e43; v=0; _tb_token_=e5fa78ae83bb3; alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82OC4wLjM0NDAuNzUgU2FmYXJpLzUzNy4zNg%3D%3D; cookie32=6b7003b7a3cd46f42ab809c97c0e5e8c; alimamapw=FXNdEXp4Q3VXRnghVgoUVF5ZVzhUAVwNUFZWVAkBBFJYAlJRAFJXAwsKBAZWUl9XAAEEUg%3D%3D; cookie31=MTE0MjQ2NjM2LCVFOCVCNCVBRCVFNCVCOCU5Q2dvdWRvbmcscmViYXRlQGdvdWRvbmcuY29tLFRC; login=URm48syIIVrSKA%3D%3D; rurl=aHR0cHM6Ly9wdWIuYWxpbWFtYS5jb20v; x5sec=7b22756e696f6e2d7075623b32223a223636326331373934303961373534626430326636633132656339353762646135434e725a2b746f46454e693073386141772f724b4d673d3d227d; JSESSIONID=80F73EDCCFC63EC5A8E27095D4E1A05D; isg=BM3NGWiEqvJJ-g6fVM-kGyv73OmHAgvATsVvNA9SCWTTBu241_oRTBuQdNrFxhk0',
            'refer': 'https://pub.alimama.com/promo/search/index.htm?q=%E7%94%B7%E9%9E%8B&_t=1532934172077&toPage=1&perPageSize=50',
            'x-requested-with': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        params = {
            'q': '男鞋',
            '_t': '1532934172077',
            'toPage': 1,
            'perPageSize': 50,
            'auctionTag': 'shopTag: yxjh',
            't': 1532935589835,
            '_tb_token_': 'e5fa78ae83bb3',
            'pvid': '10_115.190.248.241_515_1532935589260',
        }
        url = self.base_url + urlencode(params)
        try:
            re = requests.get(url, headers=headers)
            if re.status_code == 200:
                return re.json()
        except Exception:
            print('connect error')


if __name__ == '__main__':
    print(Getter().run())
