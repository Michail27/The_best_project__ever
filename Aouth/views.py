import webbrowser
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class MyPageButton(View):
    def get(self, request):
        return render(request, 'button.html',)


client_id = '50a1d637027e17b59c16'
client_secret = 'e577b2760e4e77b27f396b975d8a9a3d36384e1a'


def git_button(request):
    code = request.GET.get('code')
    exchange_code_url = 'https://github.com/login/oauth/access_token'
    response = requests.post(exchange_code_url, {'client_id': client_id, 'client_secret': client_secret, 'code': code})
    token = response.text[13:-25]
    connections_url = 'https://api.github.com/user'
    response = requests.get(connections_url, headers={'Authorization': 'token ' + token})
    json_response = response.json()
    login = json_response['login']
    req = requests.get("https://api.github.com/users/" + login + "/repos").json()
    list_repozitoriy = []
    for name in req:
        list_repozitoriy.append(name['name'])
    output = "{0}".format(list_repozitoriy)
    return HttpResponse(output)

# requests.get("https://api.github.com/users/bogdankozlovskiy/repos").json()