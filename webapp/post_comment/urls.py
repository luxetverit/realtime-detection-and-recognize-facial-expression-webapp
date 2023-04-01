from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('',views.index, name='index'),
    path('demo/', views.demo, name="demo"),
    path('service/', views.service, name="service"),
    path('chart', views.line_chart, name='line_chart'),
    path('chartJSON', views.line_chart_json, name='line_chart_json'),
    path('qna/', views.post_list, name='qna'),
    path('qna/<int:pk>/', views.detail, name='detail'),
    path('answer/create/<int:pk>/', views.comments_create, name='comments_create'),
    path('post/create/', views.posts_create, name='posts_create'),
    path('post/modify/<int:pk>/', views.posts_modify, name='posts_modify'),
    path('post/delete/<int:pk>/', views.posts_delete, name='posts_delete'),
    path('comment/modify/<int:pk>/', views.comments_modify, name='comments_modify'),
    path('comment/delete/<int:pk>/', views.comments_delete, name='comments_delete'),

]