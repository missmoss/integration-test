#!/usr/bin/env python

from core.util import get_bourl, get_worker
from core.util import expire_handler, get_eventq, Event, Error
from core.const import *

from multiprocessing import Process
from threading import Timer

import logging
import sys

def make_worker(queue, job_id, bourl, target):
    p = Process(target=target, kwargs={'job_id': job_id, 'queue': queue, 'bourl': bourl})
    p.daemon = True
    p.start()

def make_timer(queue, job_id):
    t = Timer(WORKER_TIMEOUT, expire_handler(queue, job_id))
    t.daemon = True
    t.start()
    return t

def main(runner=1, target=None):
    bourl = get_bourl()
    expired = {}
    q = get_eventq()
    for r in xrange(runner):
        make_worker(q, r, bourl, target)
        expired[r] = make_timer(q, r)
    try:
        while True:
            ev = q.get()
            if isinstance(ev, Error):
                ev.exception()
            else:
                job_id = ev.job_id
                expired[job_id].cancel()
                expired[job_id] = make_timer(q, job_id)
                logging.info("[%d]: job alive", job_id)
    except Exception as err:
        logging.exception(err)
        sys.exit(1)

if __name__ == '__main__':
    from cmd.select import work
    main(runner=get_worker(), target=work)
