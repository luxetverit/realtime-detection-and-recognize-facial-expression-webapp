from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('',views.index, name='index'),
    path('demo/', views.demo, name="demo"),
    path('service/', views.service, name="service"),
    path('chart', views.line_chart, name='line_chart'),
    path('chartJSON', views.line_chart_json, name='line_chart_json'),
    path('qna/', views.qna, name='qna'),
    # path('detail/', views.detail, name='detail'),
    path('qna/<int:board_id>/', views.detail, name='detail'),
    path('answer/create/<int:board_id>/', views.Comments_create, name='comments_create'),
    path('post/create/', views.Posts_create, name='posts_create'),
    path('post/modify/<int:board_id>/', views.Posts_modify, name='posts_modify'),
    path('post/delete/<int:board_id>/', views.Posts_delete, name='posts_delete'),
    path('comment/modify/<int:answer_id>/', views.Comments_modify, name='comments_modify'),
    path('comment/delete/<int:answer_id>/', views.Comments_delete, name='comments_delete'),

]