from urlparse import urlunparse
import os

__bourl = None

def get_bourl():
    global __bourl
    if __bourl is None:
        host = os.environ["BIGOBJECT_HOST"]
        port = os.environ["BIGOBJECT_PORT"]
        __bourl = urlunparse(('http', host + ':' + port, '/cmd', '', '', ''))
    return __bourl

__worker_count = None

def get_worker():
    global __worker_count
    if __worker_count is None:
        __worker_count = int(os.environ["WORKER"])
    return __worker_count

##############################################################################

from multiprocessing import Queue

__eventq = Queue()

class Event(object):
    def __init__(self, job_id):
        self._job_id = None
        self.job_id = job_id
    @property
    def job_id(self):
        return self._job_id
    @job_id.setter
    def job_id(self, job_id):
        self._job_id = job_id

class Error(Event):
    def __init__(self, job_id, msg):
        Event.__init__(self, job_id)
        self.msg = msg
    def exception(self):
        raise Exception("[%d]: %s" % (self.job_id, self.msg))

def expire_handler(queue, job_id):
    expire = Error(job_id, "keep alive signal failed")
    q = queue
    def _expire():
       q.put(expire)
    return _expire

def get_eventq():
    return __eventq

##############################################################################

import logging

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logging.getLogger().setLevel(logging.WARNING)

##############################################################################

import json

def json_stream(fp):
    for line in fp:
        yield json.loads(line)

def get_content(stream):
    for obj in stream:
        data = obj.get('Content', {})
        err = obj.get('Err', "bad response: no Err")
        yield (data.get('content'), data.get('index'), err)

def validate(content):
    records, index, err = content
    if err:
        raise Exception(err)
    if records is None:
        raise Exception("bad response: no content")
    if index is None:
        raise Exception("bad response: no index")
    return (records, index)
