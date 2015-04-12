import sys
import os
import time
from redis import Redis
from rq import Queue
from rq.job import Job

_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, _dir)

if __name__ == "__main__":
    from handlers import count_words_at_url
    conn = Redis(host="192.168.59.103")
    q = Queue(connection=conn)
    job = q.enqueue(count_words_at_url, 'http://www.baidu.com')

    print "job id is ", job.id

    waiting_job = Job(connection=conn, id=job.id)

    while True:
        if waiting_job.is_queued:
            print "job is in queue"
        if waiting_job.is_started:
            print "job has been started"
        if waiting_job.is_finished:
            print "job has finished"
            print "job result is", waiting_job.result
            break
        time.sleep(1)
