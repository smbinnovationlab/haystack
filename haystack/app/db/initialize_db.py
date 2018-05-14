# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from db.mysql_conf import mysql_conf, mysql_engine
from db.object_definition import Base
from sqlalchemy import create_engine


def init_db():
    # Connect to mysql
    engine = create_engine('mysql+pymysql://%s:%s@%s:%s'
                           % (mysql_conf['user'],
                              mysql_conf['passwd'],
                              mysql_conf['host'],
                              mysql_conf['port']))

    database_name = mysql_conf['db']
    # Check database
    existing_databases = engine.execute("SHOW DATABASES;")
    existing_databases = [d[0] for d in existing_databases]
    # Create database if not exists
    if database_name not in existing_databases:
        sql = 'CREATE DATABASE IF NOT EXISTS %s' % database_name
        engine.execute(sql)
        print('Database created')
    else:
        print('Database already exist')

    # Create schema
    db_engine = mysql_engine()
    Base.metadata.create_all(db_engine)
