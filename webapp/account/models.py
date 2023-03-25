from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, verbose_name='전화번호')
    password = models.CharField(max_length=256, verbose_name='비밀번호')
    email = models.CharField(max_length=255,verbose_name='이메일')

    def new_user(self, userid, name, phone, password):
        user = User.objects.create_user(name, None, password)
        user.phone = phone
        user.save()

    def superUser(self, name, password):
        user = User.objects.create_superuser(name, None, password).save()

    def auth(self, userid, password):
        user = authenticate(userid=userid, password=password)
        if user is not None:
            return user
        else:
            return None

    def __str__(self):
        return self.userid
    
    # DB 테이블 이름
    class Meta:
        db_table = 'user'

    USERNAME_FIELD = 'userid' # userid를 username로 사용
    REQUIRED_FIELDS = ['email', 'username'] 