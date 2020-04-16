#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'cache.py'

import redis
from utils import Config


class RedisManager(object):
    """docstring for RedisManager"""
    __client = None
    __pool = None
    redis_url_template = "redis://{username}:{password}@{host}:{port}/0"
    def __init__(self, password, username="", host='localhost', port=6379, **kwargs):
        super(RedisManager, self).__init__()

        url_args = {
            'username': username,
            'password': password,
            'host': host,
            'port': port
        }
        self.redis_url = self.redis_url_template.format(**url_args)
        self.__pool = redis.ConnectionPool.from_url(self.redis_url, **kwargs)
        self.__client = redis.Redis(connection_pool = self.__pool)

    def hset(self, key, field, value, expired_in_seconds=0):
        r = self.__client
        pipline = r.pipeline()
        pipline.hset(key, field, value)
        if expired_in_seconds > 0:
            pipline.expire(key, expired_in_seconds)
        pipline.execute()

    def hexists(self, name , key):
        return self.__client.hexists(name, key)

    def hget(self, name, key):
        return self.__client.hget(name, key)

    def release_connections(self):
        if self.__pool:
            self.__pool.disconnect()



