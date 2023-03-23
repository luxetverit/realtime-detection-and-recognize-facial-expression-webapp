from django.urls import path
from . import views

urlpatterns = [
    path('', views.close, name='close'),
    path('process_frame/', views.process_frame, name='process_frame'),
    path('webcam_feed/', views.webcam_feed, name='webcam_feed'),
    
]
