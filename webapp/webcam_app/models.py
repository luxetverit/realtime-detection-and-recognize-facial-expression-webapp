from django.db import models
from django.contrib.auth import authenticate
import datetime as dt
from account.models import User
from django.db import models

now=dt.datetime.now()
class Counseling(models.Model):
    userid =models.ForeignKey(User,on_delete=models.CASCADE) #상담자
    customername =models.CharField(max_length=20) # 상담받는 고객
    counsel_subject=models.CharField(max_length=50) # 상담주제 
    content=models.TextField() # 상담내용 
    raw_data=models.FileField(upload_to="cam/",blank=True) #원본자료 실시간 X
    storage_data=models.FileField(upload_to="cam/",blank=True) # 저장할 위치 
    legacy_data=models.URLField(blank=True) # 저장된 위치 
    create_at = models.DateTimeField(auto_now_add=True) # 상담일 
    
    
    def __str__(self): #상담자 
        return self.userid
    
    def auth(self,userid) :
        user = authenticate(userid=userid)
        if user is not None:
            return user
        else:
            return None
    
    class Meta:
        db_table = 'counselor_content'
        
    # USERNAME_FIELD = 'userid'
    
class Detected(models.Model):
    cost= models.OneToOneField(Counseling,on_delete=models.CASCADE,primary_key=True)
    name=f'{now.year}/{now.month}/{now.day}/{now.hour}/{Counseling.customername}'
    anger=models.IntegerField()
    anxiety=models.IntegerField()
    embarrassed=models.IntegerField()
    hurt=models.IntegerField()
    neutral=models.IntegerField()
    pleasure=models.IntegerField()
    sad=models.IntegerField()
    class Meta:
        db_table = 'detected'