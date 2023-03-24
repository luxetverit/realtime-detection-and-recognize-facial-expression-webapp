from django.urls import path
from . import views

urlpatterns = [
    path('', views.close, name='close'),
    path('webcam_feed/', views.webcam_feed, name='webcam_feed'),
    path('socket/',views.socket),
    
]
