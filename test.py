#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'test.py'

import decimal
from utils import Config
from repository import DBManager, add_trading_record
from cache import RedisManager


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


if __name__ == '__main__':
    a = decimal.Decimal('3.14')
    b = decimal.Decimal.from_float(0.5)
    print(a+b)
