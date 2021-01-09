from celery import shared_task
from time import sleep

@ shared_task
def hello(pause):
    sleep(pause)
    return 'hello, task done'