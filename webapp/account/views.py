from django.shortcuts import render
from django.contrib import auth
from django.db import connection
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from account.models import User
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now

# 회원가입
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            userid = request.POST['userid'],
            username = request.POST['username'],
            password = request.POST['password1'],
            email = request.POST['email'],

            string = "INSERT INTO user(is_superuser, email, is_staff, is_active, date_joined, userid, username, password) VALUES (0, %s, 0, 1, NOW(), %s, %s, %s)"
            return HttpResponse(string)
            cursor = connection.cursor()
            user = cursor.execute(string, [email, userid, username, password])
            
            
            auth.login(request, user)
            return redirect('/')
        return render(request, 'signup.html')
    return render(request, 'signup.html')


def signup_orm(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            userid = request.POST['userid'],
                                            username = request.POST['username'],
                                            password = request.POST['password1'],
                                            email = request.POST['email'],)
            auth.login(request, user)
            return redirect('/')
        return render(request, 'signup.html')
    return render(request, 'signup.html')
