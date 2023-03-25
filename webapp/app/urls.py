from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('',views.index, name='index'),
    path('demo/', views.demo, name="demo"),
    path('service/', views.service, name="service"),
    path('profile/', views.profile, name="profile"),
    path('profile/userinfo/', views.userinfo, name="userinfo"),
    path('password/', views.password, name='password'),
    path('qna/', views.password, name='qna'),
    # path('chart', views.line_chart, name='line_chart'),
    # path('chartJSON', views.line_chart_json, name='line_chart_json'),
]