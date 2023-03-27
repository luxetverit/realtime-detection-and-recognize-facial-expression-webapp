from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "webcam"
urlpatterns = [
    path('', views.socket, name='cam'),
    # path('webcam_feed/', views.webcam_feed, name='webcam_feed'),
    # path('socket/',views.socket),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
