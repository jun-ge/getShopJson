# -*- coding: utf-8 -*-
# !/usr/bin/env python


import json
import random
import time

import redis
import sys

from setting import REDIS_HOST, REDIS_PORT


class RedisClient(object):
    """
    Reids client
    """

    def __init__(self,  host=REDIS_HOST, port=REDIS_PORT):
        """
        init
        :param host:
        :param port:
        :return:
        """
        self.date = time.strftime("%Y%m%d%H")
        self.__conn = redis.Redis(host=host, port=port, db=0)

    def add(self, jsonData):
        self.__conn.set(self.date, jsonData)

    def add_cookie_to_right(self, cookie):
        self.__conn.rpush('cookie_list', cookie)

    def add_cookie_to_left(self, cookie):
        self.__conn.lpush('cookie_list', cookie)

    def get_cookie_from_right(self):
        return self.__conn.rpop('cookie_list')

    def len_cookie(self):
        return self.__conn.llen('cookie_list')

    def del_cookie(self):
        self.__conn.delete('cookie')

    def get(self):
        """
        get random result
        :return:
        """
        key = self.__conn.hgetall(name=self.name)
        # return random.choice(key.keys()) if key else None
        # key.keys()在python3中返回dict_keys，不支持index，不能直接使用random.choice
        # 另：python3中，redis返回为bytes,需要解码
        rkey = random.choice(list(key.keys())) if key else None
        if isinstance(rkey, bytes):
            return rkey.decode('utf-8')
        else:
            return rkey
            # return self.__conn.srandmember(name=self.name)

    def put(self, key):
        """
        put an  item
        :param value:
        :return:
        """
        key = json.dumps(key) if isinstance(key, (dict, list)) else key
        return self.__conn.hincrby(self.name, key, 1)
        # return self.__conn.sadd(self.name, value)

    def getvalue(self, key):
        value = self.__conn.get(key)
        return value if value else None

    def pop(self):
        """
        pop an item
        :return:
        """
        key = self.get()
        if key:
            self.__conn.hdel(self.name, key)
        return key
        # return self.__conn.spop(self.name)

    def delete(self, key):
        """
        delete an item
        :param key:
        :return:
        """
        self.__conn.hdel(self.name, key)
        # self.__conn.srem(self.name, value)

    def inckey(self, key, value):
        self.__conn.hincrby(self.name, key, value)

    def getAll(self):
        # return self.__conn.hgetall(self.name).keys()
        # python3 redis返回bytes类型,需要解码
        if sys.version_info.major == 3:
            return [key.decode('utf-8') for key in self.__conn.hgetall(self.name).keys()]
        else:
            return self.__conn.hgetall(self.name).keys()
            # return self.__conn.smembers(self.name)

    def get_status(self):
        return self.__conn.hlen(self.name)
        # return self.__conn.scard(self.name)

    def changeTable(self, name):
        self.name = name


if __name__ == '__main__':
    redis_con = RedisClient()
    redis_con.add_cookie_to_right('_tb_token_=efe88b7733568;t=3fa666b424fd4f18b3f561e4e88cea17;sg=g6d;cna=UbDpEzMJ7kECAdOhpzfUqUyl;cookie2=12c58d2c22c303bed0aed76207b1b73e;_l_g_=Ug%3D%3D;v=0;uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=VT5L2FSpdiNT&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTfKLc16IYwuw%3D%3D&tag=8&lng=zh_CN;unb=2849487666;skt=ee4f4c4b597fdb77;cookie1=VyguQNX5qXZE3MdCEK3QrrKVkZUz5Q2XbyEaXQJSV7k%3D;csg=8896b9d9;uc3=vt3=F8dBzrmTf9JY%2FXYwqL4%3D&id2=UUBc8nM%2F1bcGiQ%3D%3D&nk2=2jUtnF6NttehK5M%3D&lg2=W5iHLLyFOGW7aA%3D%3D;existShop=MTUzMzE5OTI3OA%3D%3D;tracknick=%5Cu8D2D%5Cu4E1Cgoudong;lgc=%5Cu8D2D%5Cu4E1Cgoudong;_cc_=VT5L2FSpdA%3D%3D;mt=ci=45_1;dnk=%5Cu8D2D%5Cu4E1Cgoudong;_nk_=%5Cu8D2D%5Cu4E1Cgoudong;cookie17=UUBc8nM%2F1bcGiQ%3D%3D;tg=0;_mw_us_time_=1533199279335;isg=BH5-h0riqUvHXf1vmqafy3KjxJQAF0iFrIFc9iiH6kG8yx6lkE-SSaSpR96iczpR;thw=cn')

    redis_con.add_cookie_to_right('_tb_token_=7e647ea05db3e;t=8e5fa575483742d8786a8135ba0bc7e5;sg=g6d;cna=I53pExmQ9x4CAdOhpzc6kHm0;cookie2=1178a3d8e8e81c239c1ffbbcdd6d6f41;_l_g_=Ug%3D%3D;v=0;uc1=cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=URm48syIZxx%2F&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTfKLc15RWtbQ%3D%3D&tag=8&lng=zh_CN;unb=2849487666;skt=4811356f98ad5077;cookie1=VyguQNX5qXZE3MdCEK3QrrKVkZUz5Q2XbyEaXQJSV7k%3D;csg=459ed28a;uc3=vt3=F8dBzrmTfpLAPFz4lyc%3D&id2=UUBc8nM%2F1bcGiQ%3D%3D&nk2=2jUtnF6NttehK5M%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D;existShop=MTUzMzE5NDMyNQ%3D%3D;tracknick=%5Cu8D2D%5Cu4E1Cgoudong;lgc=%5Cu8D2D%5Cu4E1Cgoudong;_cc_=WqG3DMC9EA%3D%3D;mt=ci=45_1;dnk=%5Cu8D2D%5Cu4E1Cgoudong;_nk_=%5Cu8D2D%5Cu4E1Cgoudong;cookie17=UUBc8nM%2F1bcGiQ%3D%3D;tg=0;_mw_us_time_=1533194326558;thw=cn;isg=BJ-foGrlODRN3Twojj5yrLbRJfPprPkadVpdcTHsO86VwL9COdSD9h2Shhkb2Mse')