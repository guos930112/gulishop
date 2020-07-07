# -*- coding: utf-8 -*-
"""
@Time   ： 2020/6/30 1:06 下午
@Author ： guos
@File   ：env_config.py
@IDE    ：PyCharm

"""
ENV_DEV = 'DEV'  # 开发环境
ENV_TEST = 'TEST'  # 测试环境
ENV_PROD = 'PROD'  # 生成环境

CUR_ENV = ENV_TEST

if CUR_ENV=='DEV':
    API_REQUEST_HOST_FROM = 'localhost'
    IS_DEBUG = False

    OA_SUPPORT_SERVER_PORT = 3000
    BOOTSTRAP_SERVERS = ['localhost:9092', ]
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379

    LOG_DIR = './log'

    DATA_RPC_PORT = 3100
    DATA_RPC_HOST = '127.0.0.1'

elif CUR_ENV==ENV_TEST:
    IS_DEBUG = False
    OA_SUPPORT_SERVER_PORT = 3000

    BOOTSTRAP_SERVERS = ['172.31.31.96:9092', ]
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379

    LOG_DIR = './log'

    DATA_RPC_PORT = 3100
    DATA_RPC_HOST = '127.0.0.1'
elif CUR_ENV==ENV_PROD:
    IS_DEBUG = False
    OA_SUPPORT_SERVER_PORT = 3000

    REDIS_HOST = '172.31.36.38'
    REDIS_PORT = 6379

    LOG_DIR = '/data/efs/log'

    DATA_RPC_PORT = 3100
    DATA_RPC_HOST = '172.31.36.38'
else:
    assert(CUR_ENV or "Must define %s! env" % CUR_ENV)
    exit(1)

LOG_DIR_GULISHOP_SERVER = LOG_DIR