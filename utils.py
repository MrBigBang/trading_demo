#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'utils.py'

import os
import configparser
import json
from datetime import date, datetime
from decimal import Decimal



class Config(object):
    """
    # Config().get_content("db_cofigs")
    配置文件里面的参数
    [db_cofigs]
    host = 127.0.0.1
    port = 3306
    user = root
    password = xxx
    """
    def __init__(self, config_filename="conf/application.cnf"):
        file_path = os.path.join(os.path.dirname(__file__), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


def unix_time(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    #convert to timestamp
    timestamp = int(time.mktime(timeArray))
    return timestamp


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
