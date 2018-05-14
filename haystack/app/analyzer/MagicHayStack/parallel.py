import logging
from multiprocessing import Pool, Manager, TimeoutError

from . import config
from .get_price import get_price

_work_manager = None
_log_queue = None


class LogExitFlag:
    """
    Flag class as hint for logging process to exit
    """
    pass


def parallel_log():
    """
    Logger process for parallel processes, exit on receiving LogExitFlag instance
    :return:
    """
    manual_log = open('tmp/parallel.log', 'a')
    while True:
        obj = _log_queue.get()
        if isinstance(obj, LogExitFlag):
            break
        manual_log.write(obj)
        print('logged')
        manual_log.flush()
    manual_log.close()


def logged_get_price(params):
    """
    decorated get_price interface with logging
    :param params:
    :return:
    """
    ret = get_price(*params)
    logging.info(ret)
    _log_queue.put(params[0] + '\n' + str(ret) + '\n')
    return ret


def parallel_get_price(urls, image_urls, record=None, n_processes=6):
    """
    Get price in parallel, only urls is a list compared to get_price interface
    :param urls: [str]
    :param image_urls: [str]
    :param record: str_path
    :param n_processes: int, how many processes (browsers) is used
    :return: [[(price:str, currency:str, weight:float), ...], ...], return in same order given
    """
    global _work_manager, _log_queue            # lazy loading to avoid process problem
    if _work_manager is None:
        _work_manager = Manager()
        _log_queue = _work_manager.Queue()

    logging.basicConfig(level=logging.INFO)
    pool = Pool(processes=n_processes + 1)      # add one for log listener
    pool.apply_async(parallel_log)
    n_jobs = len(urls)
    handler = [None] * n_jobs
    results = [None] * n_jobs
    # manual_log.write('Starting %d processes on %d jobs\n' % (n_processes, n_jobs))

    # add jobs to the pool
    for i in range(n_jobs):
        params = urls[i], image_urls, record
        handler[i] = pool.apply_async(logged_get_price, (params, ))

    # pool running, join all results
    for i in range(n_jobs):
        results[i] = []                 # if exception
        try:
            results[i] = handler[i].get(timeout=config.PARALLEL_TIMEOUT)
        except TimeoutError:
            logging.warning('Timeout for %s' % urls[i])
        except Exception as e:
            logging.warning(e)
        print(urls[i], results[i])
    pool.close()
    _log_queue.push(LogExitFlag())
    return results


def test():
    urls = list(map(lambda x: x.strip(), open('analyzer/MagicHayStack/data/puf.txt').readlines()))
    parallel_get_price(urls, ['a.jpg'], record=config.RECORD_FILE)

