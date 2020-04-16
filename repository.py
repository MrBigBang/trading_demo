#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'repository.py'

import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from utils import Config, JSONEncoder
from log import logger
import decimal
from threading import Lock



class DBManager(object):

    __lock = Lock()
    __pool = None
    """docstring for DBManager"""
    def __init__(self, host='localhost', user=None, pwd="", db=None, port=3306,  ** kwargs):
        super(DBManager, self).__init__()
        self.db_host = host
        self.db_port = int(port)
        self.db_user = user
        self.db_pwd = pwd
        self.db_schema = db

    def __get_conn(self):
        self.__init_pool()
        return DBManager.__pool.connection()

    def __init_pool(self):
        with self.__lock:
            if DBManager.__pool is None:
               DBManager.__pool = PooledDB(creator=pymysql,
                mincached=1,
                maxcached=20,
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                passwd=self.db_pwd,
                db=self.db_schema,
                use_unicode=True,
                charset="utf8",
                cursorclass=DictCursor,
                autocommit=False)

    def __execute(self, sql, param=None):
        db_conn = self.__get_conn()
        cursor = db_conn.cursor()
        try:
            count = cursor.execute(sql, param)
            db_conn.commit()
        finally:
            cursor.close()
            db_conn.close()
        return count

    def getAll(self, sql, param=None):
        db_conn = self.__get_conn()
        cursor = db_conn.cursor()
        try:
            count = cursor.execute(sql, param)
            if count > 0:
                result = cursor.fetchall()
            else:
                result = None
        finally:
            cursor.close()
            db_conn.close()

        return result

    def getOne(self, sql, param=None):
        db_conn = self.__get_conn()
        cursor = db_conn.cursor()
        try:
            count = cursor.execute(sql, param)
            if count > 0:
                result = cursor.fetchone()
            else:
                result = None
        finally:
            cursor.close()
            db_conn.close()

        return result

    def getMany(self, sql, num, param=None):
        db_conn = self.__get_conn()
        cursor = db_conn.cursor()
        try:
            count = cursor.execute(sql, param)
            if count > 0:
                result = cursor.fetchmany(num)
            else:
                result = None
        finally:
            cursor.close()
            db_conn.close()

        return result

    def update(self, sql, param=None):
        return self.__execute(sql, param)

    def insert(self, sql, param=None):
        return self.__execute(sql, param)

    def delete(self, sql, param=None):
        return self.__execute(sql, param)

    def do_transaction(self, execute_method, **kwargs):
        db_conn = self.__get_conn()
        cursor = db_conn.cursor()
        try:
            db_conn.begin()
            result = execute_method(cursor, **kwargs)
        except Exception as e:
            logger.error("Unexpected error:", sys.exc_info()[0])
            db_conn.rollback()
            # TODO raise exception
            result = None
        else:
            db_conn.commit()
        finally:
            cursor.close()
            db_conn.close()
        return result


    def close(self):
        DBManager.__pool.close()


def add_trading_record(cursor, **kwargs):
    count = cursor.execute("select * from account_info where id=%s for update", kwargs['user_id'])
    if count > 0:
        result = cursor.fetchone()
    cursor.execute("insert into trading_records (user_id, trade_amount) values (%s, %s);", [kwargs['user_id'], kwargs['trading_amount']])
    #update
    cursor.execute("update account_info set balance=balance+%s where id=%s", [kwargs['trading_amount'], kwargs['user_id']])
    result['balance'] = result['balance'] + decimal.Decimal(kwargs['trading_amount'])
    return result




