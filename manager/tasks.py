from celery import shared_task
from time import sleep
from requests import get, post
from manager.models import Repozitors


# @ shared_task
# def hello(pause):
#     sleep(pause)
#     return 'hello, task done'



@ shared_task
def update_repozitor():
    list_rep = Repozitors.objects.all()
    for rep in list_rep:
        login = rep.git_login
        user = rep.user_id
        req = get(f"https://api.github.com/users/{login}/repos")
        repos = [i['name'] for i in req.json()]
        Repozitors.objects.filter(user_id=user).update(
            user_id=user, text=repos, git_login=login)
    return 'Dane'