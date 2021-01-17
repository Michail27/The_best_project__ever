from celery import shared_task
from time import sleep
from requests import get, post
from manager.models import Repozitors

@ shared_task
def update_repozitor():
    git_hab_users = Repozitors.objects.all()
    for user in git_hab_users:
        login = user.github_account
        response = get(f"https://api.github.com/users/{login}/repos")
        repos = [i['name'] for i in response.json()]
        user.github_repos = repos
        user_id = user.user_id
        Repozitors.objects.all().filter(user_id=user_id).update(
            user_id=user_id, _github_repos=repos, github_account=login)
    return 'Dane'
