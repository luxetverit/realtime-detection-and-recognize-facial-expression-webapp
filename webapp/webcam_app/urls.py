from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.socket, name='socket'),
    # path('webcam_feed/', views.webcam_feed, name='webcam_feed'),
    # path('socket/',views.socket),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
