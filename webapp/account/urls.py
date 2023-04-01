from django.urls import path 
from . import views

app_name = "account"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name="profile"),
    path('profile/userinfo/', views.userinfo, name="userinfo"),
    path('password/', views.password, name='password'),
]

