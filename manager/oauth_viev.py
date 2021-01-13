
from django.shortcuts import render, redirect
from requests import post, get
from manager.models import Repozitor

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
    list_rep = Repozitor.objects.filter(user=request.user.id)
    if list_rep:
        Repozitor.objects.update(user=request.user, text=repos)
    else:
        Repozitor.objects.create(user=request.user, text=repos)
    return redirect('profil')
