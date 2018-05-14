# -*- coding:utf-8 -*-

import os
import sys

sys.path.append('..' + os.path.sep)

from db.db_operations import modify_event_time_up_to_date


if __name__ == '__main__':
    try:
        modify_event_time_up_to_date(sys.argv[1], sys.argv[2])  # argv[1]: mysql host, argv[2] mysql password
    except Exception as e:
        print(str(e))
    finally:
        print('[V] done')
