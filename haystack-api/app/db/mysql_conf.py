# -*- coding:utf-8 -*-

from sqlalchemy import create_engine


mysql_conf = {
    'host': 'api_db',
    'port': '3306',
    'user': 'root',
    'passwd': 'test',
    'db': 'haystack_api',
    'charset': 'utf8mb4',
}


def mysql_engine():
    engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=%s'
                           % (mysql_conf['user'],
                              mysql_conf['passwd'],
                              mysql_conf['host'],
                              mysql_conf['port'],
                              mysql_conf['db'],
                              mysql_conf['charset']))
    return engine
