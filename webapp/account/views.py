from django.shortcuts import render
from django.contrib import auth
from django.db import connection
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from account.models import User
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.contrib.auth import logout,login

# 로그인 기능 구현
def Login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = User.auth(email, password)

        if user is not None:
            print("인증성공")
            login(request,user)
        else:
            print("인증실패") 
        
        return render(request, 'login.html')

def Logout(request):
    logout(request)
    return render(request, 'login.html')

# 회원 가입 기능 구현
def signup(request):
    data = {}
    if request.method == 'GET':
        data['page'] = '회원가입'
        return render(request, 'password.html', data)
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        print(f'{username} {email} {password}')

        user = User()
        user.new_user(username, email, password)
        return render(request, 'login.html', data)
