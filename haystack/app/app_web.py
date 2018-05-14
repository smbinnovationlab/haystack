# -*- coding:utf-8 -*-

import sys
sys.path.append('.')

from run_backend import app_web
from db.initialize_db import init_db

import time


while True:
    try:
        init_db()
        break
    except Exception as e:
        print(e)
    time.sleep(10)


if __name__ == '__main__':
    app_web.run(host='0.0.0.0', port=8000, debug=True)
