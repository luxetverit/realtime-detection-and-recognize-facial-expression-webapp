from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "webcam"

urlpatterns = [
    
    path('',views.index,name='index'),
    path('list/', views.CounselingListView.as_view(), name='counseling_list'),
    path('list/<int:pk>/', views.CounselingDetailView.as_view(), name='counseling_detail'),
    path('list/form/', views.counseling_add, name='counseling_add'),
    path('list/edit/<int:pk>/', views.counseling_edit, name='counseling_edit'),
    path('list/delete/<int:pk>/', views.counseling_delete, name='counseling_delete'),
    path('realtime/<int:pk>', views.socket, name='realtime'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
