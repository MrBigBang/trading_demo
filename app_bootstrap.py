#!/usr/bin/env python3
#
#
# 'app_bootstrap.py'
#
#  author: li.d
#
#

import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from handlers import DefaultHandler, BalanceHandler, RecordHandler
from log import logger
from cache import RedisManager
from repository import DBManager
from utils import Config


define("port", default=8989, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self, db_mng, redis_mng):
        self.db_mng = db_mng
        self.redis_mng = redis_mng
        handlers = [
            (r"/", DefaultHandler),
            (r"/balance", BalanceHandler),
            (r"/trading/record", RecordHandler),
        ]
        super(Application, self).__init__(handlers)



def main():
    options.parse_command_line()

    config = Config()
    # init redis
    redis_config = config.get_content("redis_configs")
    extra_args = {
        'max_connections':redis_config['maxconns']
    }
    redis_mng = RedisManager(redis_config["password"], **extra_args)
    # init db
    db_config = config.get_content("db_configs")
    db_mng = DBManager(db_config["host"], db_config["user"], db_config["password"], db_config["database"], db_config["port"])

    app = Application(db_mng, redis_mng)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
