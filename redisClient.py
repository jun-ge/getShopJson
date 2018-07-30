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
        self.date = time.strftime("%Y%m%d%H%M")
        self.__conn = redis.Redis(host=host, port=port, db=0)

    def add(self, jsonData):
        self.__conn.set(self.date, jsonData)

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
    redis_con.add('json数据')

