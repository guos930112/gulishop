# -*- coding: utf-8 -*-
"""
@Time   ： 2020/6/30 1:07 下午
@Author ： guos
@File   ：db_config.py
@IDE    ：PyCharm

"""
from config.env_config import ENV_DEV, ENV_TEST, CUR_ENV, ENV_PROD

if CUR_ENV == ENV_DEV:
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_PASSWD = 'rootguos'
elif CUR_ENV == ENV_TEST:
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_PASSWD = 'rootguos'
elif CUR_ENV == ENV_PROD:
    MYSQL_HOST = 'betaex-db.chqyadh2yhzy.ap-northeast-1.rds.amazonaws.com'
    MYSQL_PORT = 33306
    MYSQL_PASSWD = 'betaex2019todamon'
