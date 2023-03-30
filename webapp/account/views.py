from django.contrib import auth
from django.db import connection
from django.shortcuts import render, redirect
from account.models import User
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required

# 로그인
def login_view(request):
    # 주소를 입력해서 들어오는 경우
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        userid = request.POST['userid']
        password = request.POST['password']
        user = authenticate(request, userid=userid, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
            # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'message': '아이디 혹은 비밀번호가 틀렸습니다.'})
  
    
# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')
  
# 회원가입  
def signup(request):
    # 주소를 입력해서 들어오는 경우
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    elif request.method == 'POST':
        userid = request.POST['userid']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if request.POST['password'] != request.POST['password2']:
            return render(request, 'signup.html')

        user = User()
        user.new_user(userid, username, email, password)
        
        return render(request, 'login.html')


@login_required
def index(request):
    if request.user.is_superuser:
        users = get_user_model().objects.all()
        context = {
            'users':users,
        }
        return render(request, 'accounts/index.html', context)
    else:
        return redirect('articles:index')



def profile(request):
    return render(request, 'profile.html')

def userinfo(request):
    return render(request, 'userinfo.html')

def password(request):
    return render(request, 'password.html')

