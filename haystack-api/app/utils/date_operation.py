# -*- coding:utf-8 -*-

from time import mktime
import datetime
import random


def string2timestamp(s):
    dt = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    ts = mktime(dt.timetuple())
    return ts


def generate_random_date(current_str_date, number):
    generated_date = [current_str_date, ]
    current_timestamp = string2timestamp(current_str_date)
    total_day_diff = 30
    for i in range(number - 1):
        random_date_diff = random.randint(1, total_day_diff - 1)
        random_second_diff = random.randint(0, 24 * 60 * 60)
        random_timestamp = current_timestamp - random_date_diff * 24 * 60 * 60 - random_second_diff
        random_date = datetime.datetime.fromtimestamp(random_timestamp)
        generated_date.append(random_date.strftime('%Y-%m-%d %H:%M:%S'))
    return generated_date
