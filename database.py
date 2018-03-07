import pymongo
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from multiprocessing import Queue

logger = logging.getLogger('db')
log_path = "./db.log"
fh = TimedRotatingFileHandler(log_path, 'H', 6, 5)
fh.setLevel(logging.INFO)
fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(fmt)
fh.setFormatter(formatter)
logger.addHandler(fh)


class DBMange(object):
    def __init__(self, addr, port, db, coll):
        try:
            self.conn = pymongo.MongoClient('127.0.0.1', 27017)
        except Exception:
            logger('db connection error')
            exit(1)

        self.db = self.conn[db]
        self.coll = self.db[coll]

    def store(self, db_item):
        logger.info('db inserting markets')
        self.coll.insert_one(db_item)


def db_proc_start(que, config):
    logger.info('DB Process: %s' % os.getpid())
    logger.info('setting db connection')

    dbm = DBMange(
        config['db_address'],
        config['db_port'],
        config['db_name'],
        config['coll_name']
    )

    try:
        while True:
            value = que.get(True)
            dbm.store(value)
    except KeyboardInterrupt:
        logger.info('db process exit')
