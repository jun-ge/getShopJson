import json
import random
import re
import time
from _md5 import md5

from urllib.parse import urlencode
from urllib.request import urlopen

import requests
from selenium.webdriver import ActionChains

from redisClient import RedisClient


class Getter:
    def __init__(self, key='女鞋', cookie='t=42094f472057d3bf10e7ba67b0cc56bd; cookie2=1c00fb02ce4c211b537fc858916fe12d; _tb_token_=76635ee8eea7b; cna=U/A4EwU2BSYCAdOhoOPCBeFZ; v=0; alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82OC4wLjM0NDAuNzUgU2FmYXJpLzUzNy4zNg%3D%3D; cookie32=6b7003b7a3cd46f42ab809c97c0e5e8c; alimamapw=FXNdEXp4Q3VXRnghVgoUVF5ZVzhUAVwNUFZWVAkBBFJYAlJRAFJXAwsKBAZWUl9XAAEEUg%3D%3D; cookie31=MTE0MjQ2NjM2LCVFOCVCNCVBRCVFNCVCOCU5Q2dvdWRvbmcscmViYXRlQGdvdWRvbmcuY29tLFRC; _umdata=70CF403AFFD707DFCBC0A061E697231DF2FA185F3EFA4FE20AF47EAD28EA0DB6A0D728BD03756153CD43AD3E795C914CD3F74DC7A5D318DA48CE54AE84144647; 114246636_yxjh-filter-1=true; JSESSIONID=B6B162727EE75E8CE8355485D005C992; login=URm48syIIVrSKA%3D%3D; rurl=aHR0cHM6Ly9wdWIuYWxpbWFtYS5jb20v; x5sec=7b22756e696f6e2d7075623b32223a22656162393663643437623530636561373861623134326265316233323936346543494770674e7346454b4b6234702f42777144537851453d227d; apush2ec0cc1e080f6deec6ffb50a44b54f70=%7B%22ts%22%3A1533023378501%2C%22heir%22%3A1533023342233%2C%22parentId%22%3A1533019254918%7D; isg=BJOT2SGPzNrFnoDxHi0C7bG5Ihd94C22JMdhWkWxjbLpxLdm3RtqWqJS-nQP5H8C'):

        self.cookie = cookie
        self.headers = {
            # 'cookie':self.getCookie(),
            # 'refer': 'https://pub.alimama.com/promo/search/index.htm?q=%E7%94%B7%E9%9E%8B&_t=1532934172077&toPage=1&perPageSize=50',
            'x-requested-with': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }

        self.base_url = 'https://pub.alimama.com/items/search.json?'
        self.conn = RedisClient()
        self.key = key


    def getCookie(self, username='购东goudong', passwd='gd19691818'):
        from selenium import webdriver
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.wait import WebDriverWait
        # url = 'https://pub.alimama.com/'
        url = 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true'
        # url = 'https://www.alimama.com/member/login.htm'

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        browser = webdriver.Chrome()
        wait = WebDriverWait(browser, 10)

        browser.get(url)
        browser.maximize_window()


        element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_Quick2Static')))
        time.sleep(1)
        element.click()

        browser.implicitly_wait(20)
        input_username = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_username_1')))
        input_passwd = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#TPL_password_1')))
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#J_SubmitStatic')))

        slide = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#nc_1_n1z')))

        input_username.clear()
        time.sleep(1)
        input_passwd.clear()
        time.sleep(1)
        input_username.send_keys(username)
        time.sleep(1)
        input_passwd.send_keys(passwd)
        time.sleep(1)

        #nc_1_n1z
        action = ActionChains(browser)
        # for index in range(500):
        #     try:
        #         action.drag_and_drop_by_offset(slide, 500,0).perform()#平滑
        #     except Exception:
        #         break
        time.sleep(12)
        submit.click()
        print(browser.current_window_handle)

        cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        print(cookiestr)
        return cookiestr



    def run(self):
        jsonData = json.dumps([self.getJson(page) for page in range(1, 101)], ensure_ascii=False)
        # jsonData = self.getJson(1)
        # self.conn.add(jsonData)
        return jsonData


    def getJson(self, page):
        self.headers['cookie'] = self.cookie
        print(self.headers)
        t = int(time.time() * 1000)
        params = {
            'q': self.key,
            '_t': t - 120000,  # 用户登入时间戳
            'toPage': page,  # 页数
            'perPageSize': 50,  # 每页展示的数量
            'auctionTag': None,  # 作用未知
            'shopTag': 'yxjh',  # 作用未知
            't': t,  # 最近一次刷新时间戳.精确到毫秒
            '_tb_token_': '',  # 通过页面获取
            # 'pvid': '10_115.190.248.241_515_1532935589260',  # 10 + ip + 随机数（num) +
            'pvid': '10_115.190.248.241_' + str(random.randint(100, 9999)) + '_' + str(t - 650)
        }
        import re
        source = requests.get('https://pub.alimama.com/').text
        token_list = re.findall(r"input name='_tb_token_' type='hidden' value='([a-zA-Z0-9]+)'", source)
        params['_tb_token_'] = token_list[0] if token_list else ''

        url = self.base_url + urlencode(params)
        print(url)
        try:
            s = requests.session()
            res = s.get(url, headers=self.headers)

            if res.status_code == 200:
                # return res.text
                print(res.json())
                return json.dumps(res.json(), ensure_ascii=False)
        except TimeoutError:
            print('connect timeout')


if __name__ == '__main__':
    # print(time.time())
    print(Getter().getCookie())
    # print(Getter().run())
