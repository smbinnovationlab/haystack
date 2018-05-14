# -*- coding:utf-8 -*-

import sys
sys.path.append('.')

from db.initialize_db import init_db
from run_web_server import app_web_server
import time


while True:
    try:
        init_db()
        break
    except Exception as e:
        print(e)
    time.sleep(10)


if __name__ == '__main__':
    app_web_server.run(host='0.0.0.0', port=5001, debug=True)
