from django.urls import path
from . import views

# app_name = 'user'
app_name = 'app'
urlpatterns = [
    path('',views.index, name='index'),
    # path('demo/', views.demo, name="demo"),
    # path('service/', views.service, name="service"),
    # path('profile/', views.profile, name="profile"),
    # path('profile/userinfo/', views.userinfo, name="userinfo"),
    path('login/', views.login, name='login'),
    # path('password/', views.password, name='password'),
    # path('register/', views.register, name='register'),
]