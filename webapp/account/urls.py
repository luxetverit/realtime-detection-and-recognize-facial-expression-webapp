from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

# 장고 django.contrib.auth.urls 사용으로 경로 재설정함 
# app_name = "account"

urlpatterns = [
    # 장고 django.contrib.auth.urls 에서 기본으로 제공하는 유저 관리 폼
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # 장고 django.contrib.auth.urls 사용으로 경로에 'account' 재설정
    path('account/signup/', views.signup, name='signup'),
    path('account/login/', views.login_view, name='login'),
    path('account/logout/', views.logout_view, name='logout'),
    path('account/profile/', views.profile, name="profile"),
    path('account/profile/userinfo/', views.userinfo, name="userinfo"),
      
]

