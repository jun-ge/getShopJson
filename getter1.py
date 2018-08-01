import json
import random
import re
import time
from _md5 import md5

from urllib.parse import urlencode
from urllib.request import urlopen

import requests
from pyquery import pyquery
from selenium.webdriver import ActionChains, DesiredCapabilities

from redisClient import RedisClient
from taobao import Taobao
from user_agents import FakeChromeUA


class Getter:
    def __init__(self, key='女鞋'):

        self.userAgent = FakeChromeUA().get_ua()
        self.username = '购东goudong'
        # ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua = '110#MHykAUkfkeHPcKzdPK0FMuy22oLJU3y84BpeNOSUcPeWkvFIDKgvTOykJCcXkTk84KkkGTSwkPafNkgPFK2UMRykkMceB2k8eKUefcXOhwj2hQ7/8AbXowZzM1dyjwucSltV8MuQ30kghpte23vTkpc0x17Z7UpRkDxNW1oUmwckhnjf+vcIbRjIu9G0/hyGHkm3LtH+QOhdoTy2zMlsC423Bzs8ikt8hQuaAqQGdJbKsAkwsziNeV2pj9cwkP5ysLgwCTOiKc+esQkOZrkrG3SeKTKBywgEDEv/BLc2mrjQs3ciD5kkgOmOT+kO5/2btxG/s9M44yS5s3kwkfvPvbaCV9cw5wKD4TqK2wHakT6XMkMq6KJY194YzhliIcDWT8ko/bI8AP5Ir8xA3dQUZSXaBCqulW4HNloYosAgDbemsqiWanHOGIp0fjf7KaDRowwZhJo4z7yTDDYMo7Th3edR8v+h2oK9DWWH55jxVis5xfyANhB7mSd2CD/+…6AfmckCGbsKiBZu928hbLPnnyTWOxQrjBhSBetzDVpNaTJnkKX/71HlANJqkRD2zbXTJs5KsS3Wntmj9vRimreVXe5z+ip/bKr5kgCGomKu0ZGzD2QOw/vaKxvJb4lefzLwImLTNHZwlGoEFJTVCRsFigz5sEGbwB811Zq6zln+UpP4v2VMsj6bSVBJV3lUMNwJDUsLhOkj/gkwoznELXNakgJqHt3VuxX/94a9QWZgDV6eLkDLonr0bDzHbVqfdJ9pXg3v4GeWZa9cA2M0ubKbC2wW+gkYzw7FRS1c4AxVYwlgIvLRU0BWGugbnjLrGy2h7jGX62WRqYNsN/E5/19SBm9uR+aPluMSkt6CToB7L20cvM5u4hHMDQgMROpR2qtXjz/w/jmoFhAZoYeeYLoza1vHmlsuGCYo5MTFxfApmwUrVg8Sr9xqMsAK3pJp5BPU9ad4Fzk1PK2TVwfBgNdV4DQf8apgO3mTkmNQWR/x/ovVUHh2VozIX1MMqU=='

        # 密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '32d3e825e49ec23c451433fa259960b203bbc7757a4eb9a7606035efaee3cd588993e691e73477f837549f5d1ecc091b6f936fee935ecaccdff9e4630714a3fb33f364f3bbd75dd7e616def56d87d3ccf36ff01fdb6c32fac7cfa3b54aa63419e5a2cb8c64cc165fa4fb27ee1e3df256885cbaef6997712ecb15b895bba7e51c'

        self.post = {
            'ua': self.ua,
            'TPL_checkcode': '',
            'CtrlVersion': '1,0,0,7',
            'TPL_password': '',
            'TPL_redirect_url': 'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
            'TPL_username': self.username,
            'loginsite': '0',
            'newlogin': '0',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'css_style': '',
            'tid': 'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
            'support': '000001',
            'loginType': '4',
            'minititle': '',
            'minipara': '',
            'umto': 'NaN',
            'pstrong': '3',
            'llnick': '',
            'sign': '',
            'need_sign': '',
            'isIgnore': '',
            'full_redirect': '',
            'popid': '',
            'callback': '',
            'guf': '',
            'not_duplite_str': '',
            'need_user_id': '',
            'poy': '',
            'gvfdcname': '10',
            'gvfdcre': '',
            'from_encoding ': '',
            'sub': '',
            'TPL_password_2': self.password2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'allp': '',
            'oslanguage': 'zh-CN',
            'sr': '1366*768',
            'osVer': 'windows|6.1',
            'naviVer': 'firefox|35'
        }
        self.headers = {
            # 'cookie':self.getCookie(),
            # 'refer': 'https://pub.alimama.com/promo/search/index.htm?q=%E7%94%B7%E9%9E%8B&_t=1532934172077&toPage=1&perPageSize=50',
            'x-requested-with': 'XMLHttpRequest',
            'User-Agent': self.userAgent,
            # 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
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

    def getTaobaoCookie(self):
        taobao = Taobao()
        taobao.main()

    def getCookie(self, username='购东goudong', passwd='gd19691818'):
        # 模拟浏览器登入
        from selenium import webdriver
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.wait import WebDriverWait
        # url = 'https://pub.alimama.com/'
        url = 'https://login.taobao.com/member/login.jhtml?'
        # url = 'https://www.alimama.com/member/login.htm'

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')# 隐藏界面
        # browser = webdriver.Chrome(chrome_options=chrome_options)

        # 添加请求头信息
        # dcap = dict(DesiredCapabilities.CHROME)
        # dcap['chorme.page.settings.userAgent'] = self.ua
        # browser = webdriver.Chrome(desired_capabilities=dcap)
        # browser = webdriver.Chrome()
        # browser = webdriver.Ie(desired_capabilities=dcap)
        browser = webdriver.Ie()# ie 浏览器

        wait = WebDriverWait(browser, 10)

        browser.get(url)
        browser.maximize_window()

        # 选择以用户名，密码的方式进行登入，（找到目标后点击，不然抓取不到输入窗口）
        element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_Quick2Static')))

        element.click()
        time.sleep(1)

        # 获取输入用户名、密码，已及登入的按钮
        input_username = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#TPL_username_1')))
        input_passwd = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#TPL_password_1')))

        # 清空输入框里面的内容
        input_username.clear()
        input_passwd.clear()
        time.sleep(1)
        # 填写用户名，密码数据
        input_username.send_keys(username)
        input_passwd.send_keys(passwd)
        time.sleep(1)

        # 循环拖动验证码，若没有出现‘哎呀。。。’字样表示验证通过，中断循环
        while True:
            # time.sleep(10)
            slider = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#nc_1_n1z')))
            action = ActionChains(browser)
            action.click_and_hold(slider)# 点击并按住
            for index in range(10):
                try:
                    action.move_by_offset(index * 50, 0).perform()
                    # 水平拖动500
                    # action.drag_and_drop_by_offset(slider, 500, 0).perform()  # 平滑
                except Exception:
                    # 拖动超过报异常，中断循环
                    break
            action.release().perform()
            error = pyquery.PyQuery(browser.page_source)('.nc-lang-cnt').text()
            print(error)

            if error.startswith('哎呀'):
                restart = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#nocaptcha > div > span > a')))
                restart.click()
                time.sleep(1)
            else:
                break
        time.sleep(1)
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#J_SubmitStatic')))
        submit.click()

        cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        print(cookiestr)
        return cookiestr

    def run(self):
        # jsonData = json.dumps([self.getJson(page) for page in range(1, 101)], ensure_ascii=False)
        jsonData = self.getJson(1)
        self.conn.add(jsonData)
        return jsonData

    def getJson(self, page):
        # self.headers['cookie'] = self.getTaobaoCookie()
        cookie =  self.getTaobaoCookie()

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
            res = s.get(url, headers=self.headers, data=self.post, cookies=cookie)
            print(res.headers)

            if res.status_code == 200:
                return json.dumps(res.json(), ensure_ascii=False)
        except TimeoutError:
            print('connect timeout')


if __name__ == '__main__':
    # print(time.time())
    print(Getter().getCookie())
    # print(Getter().run())
