from django.urls import path 
from . import views

app_name = "account"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
<<<<<<< HEAD
    path('login/', views.login, name='login'),
]
=======
]
>>>>>>> 26c6c5a4d908d799be8873c82a7746e7e62734df
