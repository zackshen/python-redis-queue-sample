# 任务队列

## 环境准备

### Python Redis

    # pip install -i http://pypi.douban.com/simple redis

### RQ

    # pip install -i http://pypi.douban.com/simple rq

### Redis Server

	# docker pull redis:latest
	# docker run -d -p 6379:6379 -t redis:latest
	
### RqWorker

启动rqworker，等待任务

	# rqworker -P . -u redis://192.168.59.103:6379	

## 运行一个任务
	
	# python create.py
	
```
import sys
import os
import time
from redis import Redis
from rq import Queue
from rq.job import Job

_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, _dir)

if __name__ == "__main__":
    from handles import count_words_at_url
    # 连接redis服务器
    conn = Redis(host="192.168.59.103")
    # 创建RQ任务队列
    q = Queue(connection=conn)
    # 将任务处理函数和参数传入队列，这里会将任务发到redis服务器，任务创建完毕返回job实例
    job = q.enqueue(count_words_at_url, 'http://www.baidu.com')

	# 新建一个任务等待结果
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
```
