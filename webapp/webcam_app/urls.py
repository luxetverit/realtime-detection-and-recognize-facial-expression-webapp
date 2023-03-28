from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "webcam"

urlpatterns = [
    
    path('', views.counseling_list, name='counseling_list'),
    path('<int:pk>/', views.counseling_detail, name='counseling_detail'),
    path('form/', views.counseling_add, name='counseling_add'),
    path('edit/<int:pk>/', views.counseling_edit, name='counseling_edit'),
    path('delete/<int:pk>/', views.counseling_delete, name='counseling_delete'),
    path('cam', views.socket, name='cam'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
