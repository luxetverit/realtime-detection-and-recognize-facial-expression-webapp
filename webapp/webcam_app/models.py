from django.db import models

from account.models import User
from django.db import models


class Counseling(models.Model):
    userid =models.ForeignKey(User,on_delete=models.CASCADE) #상담자
    customername =models.CharField(max_length=20) # 상담받는 고객
    counsel_subject=models.CharField(max_length=50) # 상담주제 
    content=models.TextField() # 상담내용 
    raw_data=models.FileField(upload_to="cam/",blank=True) #원본자료 실시간 X
    stroage_data=models.FileField(upload_to="cam/",blank=True) # 저장할 위치 
    legacy_data=models.URLField(blank=True) # 저장된 위치 
    create_at = models.DateTimeField(auto_now_add=True) # 상담일 
    
    
    def __str__(self): #상담자 
        return self.userid
    

    
    class Meta:
        db_table = 'counselor_content'
    