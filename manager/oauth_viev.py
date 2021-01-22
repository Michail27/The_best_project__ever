
from django.shortcuts import render, redirect
from requests import post, get
from manager.models import Repozitors

GIT_CLIENT_ID = '50a1d637027e17b59c16'
GIT_CLIENT_SICRET = 'e577b2760e4e77b27f396b975d8a9a3d36384e1a'

def aouch_viev(request):
    code = request.GET.get('code')
    url = f'https://github.com/login/oauth/access_token?client_id={GIT_CLIENT_ID}&client_secret={GIT_CLIENT_SICRET}&code={code}'
    response = post(url, headers={'Accept': 'application/json'})
    access_token = response.json()['access_token']
    connections_url = 'https://api.github.com/user'
    response = get(connections_url, headers={'Authorization': f'token {access_token}'})
    json_response = response.json()
    login = json_response['login']
    req = get(f"https://api.github.com/users/{login}/repos")
    repos = [i['name'] for i in req.json()]
    if request.user.is_authenticated:
        r = Repozitors.objects.filter(user=request.user.id)
        if r:
            pass
        else:
            repozitors = Repozitors(user=request.user, github_account=login)
            repozitors.github_repos = repos
            repozitors.save()
            r = Repozitors.objects.filter(user=request.user.id)
        return render(request, 'ProfilUser.html', {'repoz': r[0].github_repos})
    return render(request, 'ProfilUser.html')
