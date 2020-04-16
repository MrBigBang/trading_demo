#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'test.py'

import decimal
from utils import Config
from repository import DBManager, add_trading_record
from cache import RedisManager
from threading import Lock, Thread, Condition
import time


def test_dbmng():
    config = Config()
    db_config = config.get_content("db_configs")
    print(db_config)
    db_mng = DBManager(db_config["host"], db_config["user"], db_config["password"], db_config["database"], db_config["port"])
    # print(db_mng.insert("insert into account_info (name, balance) values (%s, %s);", ['xiaoming', 3.0]))
    # print(db_mng.insert("insert into trading_records (user_id, trade_amount) values (%s, %s);", [3, -1]))
    # print(db_mng.getAll("select * from account_info;"))
    # kwargs = {
    #     "user_id": 4,
    #     "trading_amount": 0.5
    # }
    # db_mng.do_transaction(add_trading_record, **kwargs)
    print(db_mng.getOne("select * from account_info where id=%s", [1]))


def test_redismng():
    config = Config()
    redis_config = config.get_content("redis_configs")
    print(redis_config)
    extra_args = {
        'max_connections':redis_config['maxconns']
    }
    redis_mng = RedisManager(redis_config["password"], **extra_args)
    #print(redis_mng.hset("account_info_cache", "1", "sss", 5))
    #print(redis_mng.hexists("account_info_cache", "1"))
    print(redis_mng.hget("account_info_cache", "1"))

value = 0
lock = Lock()

def test_lock():
    threads = []
    for i in range(100):
        t = Thread(target=get_lock)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    print(value)

def get_lock():
    global value
    with lock:
        new = value + 1
        time.sleep(.01)
        value = new

class TestLock(object):
    __lock = Lock()
    __pool = None
    """docstring for TestLock"""
    def __init__(self):
        super(TestLock, self).__init__()

    def init_pool(self):
        with TestLock.__lock:
            if TestLock.__pool is None:
                print("enter init __pool")
                TestLock.__pool = '123'
    def get_pool(self):
        return self.__pool

def test_lock2():
    cond  = Condition()
    testlock = TestLock()
    def invork_init_pool():
        cond.acquire()
        try:
            cond.wait()
            testlock.init_pool()
        finally:
            cond.release()
    threads = []
    for i in range(100):
        t = Thread(target=invork_init_pool)
        t.start()
        threads.append(t)

    with cond:
        cond.notifyAll()

    for thread in threads:
        thread.join()

    print(testlock.get_pool())


if __name__ == '__main__':
    test_lock2()
