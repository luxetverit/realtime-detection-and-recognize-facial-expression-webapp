from django.db import models
from django.contrib.auth.models import AbstractUser #AbstaractUser을 상속하여 User모델 설정
# authenticate - User 인증 함수. 자격 증명이 유효한 경우 User 객체를, 그렇지 않은 경우 None을 반환
from django.contrib.auth import authenticate

# 일반 유저 모델 설정 
class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    userid = models.CharField(max_length=12,unique=True)
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=11,verbose_name='전화번호',unique=True)
    password = models.CharField(max_length=256, verbose_name='비밀번호')
    email = models.CharField(max_length=255,verbose_name='이메일',unique=True)

    def new_user(self,name,phone,password):
        user = User.objects.create_user(name,None,password)
        user.phone = phone
        user.save()

    def superUser(name,password):
        user = User.objects.create_superuser(name,None,password).save()

    def auth(phone, password):
        user = authenticate(phone=phone, password=password)
        if user is not None:
            return user
        else :
            return None
    # 유저 이름으로 보여지게 함
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user'
    
    # id로 나오게 설정 유니크한 값만 넣을 수 있음
    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['email', 'username'] 

# 질문란
class Posts(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)
    
    # 작성한 질문이 제목으로 보여지게 함
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'

# 댓글란
class Comments(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)
    
    # 작성한 답변이 제목으로 보여지게 함
    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comments'