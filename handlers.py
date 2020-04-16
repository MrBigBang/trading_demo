#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'handlers.py'

from tornado import web
from repository import add_trading_record
import json
from utils import JSONEncoder


class BaseHandler(web.RequestHandler):
    '''BaseHandler'''

    def prepare(self):
        pass

    def write_error(self):
        pass

    def set_default_headers(self):
        pass


class DefaultHandler(BaseHandler):
    """docstring for DefaultHandler"""
    def get(self):
        self.write("Trading Demo.")


class BalanceHandler(BaseHandler):
    """docstring for BalanceHandler"""
    def get(self):
        # get from cache
        user_id = self.get_argument('userid')
        cached_account_info = self.application.redis_mng.hget('account_info_cache', user_id)
        if cached_account_info:
            de_info = json.loads(cached_account_info)
            self.write(de_info['balance'])
            return
        result = self.application.db_mng.getOne("select * from account_info where id=%s", user_id)
        json_result = json.dumps(result, cls = JSONEncoder)
        self.application.redis_mng.hset("account_info_cache", user_id, json_result, 300)
        self.write(str(result['balance']))


class RecordHandler(BaseHandler):
    """docstring for RecordHandler"""

    def post(self):
        user_id = self.get_body_argument('userid')
        trading_amount = self.get_body_argument('tradingamount')
        trans_args = {
            'user_id': user_id,
            'trading_amount': trading_amount
        }
        result = self.application.db_mng.do_transaction(add_trading_record, **trans_args)
        json_result = json.dumps(result, cls=JSONEncoder)
        self.application.redis_mng.hset("account_info_cache", user_id, json_result, 300)
        self.write("Success")





