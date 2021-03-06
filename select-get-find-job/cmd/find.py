from core.const import *
from core.util import Event, Error, json_stream, get_content, validate

import random
import requests as reqs
import sys

def work(queue, job_id, bourl):
    hangup = False
    while True:
        try:
            while True:
                hangup = random.choice(TO_HANGUP_OR_NOT)
                if not hangup:
                    rtimeout = (CONN_TIMEOUT, READ_TIMEOUT)
                else:
                    rtimeout = (CONN_TIMEOUT, 0)
                r = reqs.post(bourl,
                    stream=True,
                    json={'Stmt': 'FIND 10 significant() Product.brand IN Customer.gender BY SUM(total_price) FROM sales'},
                    timeout=rtimeout
                )
                for content in get_content(json_stream(r.raw)):
                    _, index = validate(content)
                    if index == -1:
                        break
                queue.put(Event(job_id))
        except reqs.exceptions.ConnectTimeout:
            queue.put(Error(job_id, "unable to reach BigObject"))
            sys.exit(1)
        except reqs.exceptions.ReadTimeout:
            if not hangup:
                queue.put(Error(job_id, "no resp from BigObject"))
                sys.exit(1)
            else:
                queue.put(Event(job_id))
        except Exception as err:
            queue.put(Error(job_id, str(err)))
            sys.exit(1)
