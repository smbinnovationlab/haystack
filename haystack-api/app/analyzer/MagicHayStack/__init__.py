import os

from .get_price import get_price, submit_label
# from .parallel import parallel_get_price

_tmp_path = os.path.join(os.getcwd(), 'tmp/')
if not os.path.isdir(_tmp_path):
    os.mkdir(_tmp_path)
