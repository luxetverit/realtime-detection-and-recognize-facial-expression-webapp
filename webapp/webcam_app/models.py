from django.db import models
from django.contrib.auth import authenticate
from account.models import User
from django.db import models


class Counseling(models.Model):
    userid =models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True) #상담자
    customername =models.CharField(max_length=20) # 상담받는 고객
    counsel_subject=models.CharField(max_length=50) # 상담주제 
    content=models.TextField() # 상담내용 
    storage_data = models.FileField(upload_to="cam/", blank=True)  
    download_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    
    
    def __str__(self): #상담자 
        return self.user.userid
    

    
    class Meta:
        db_table = 'counseling'
        
    # USERNAME_FIELD = 'userid'
    
class DetectedEmotions(models.Model):
    counseling = models.OneToOneField(Counseling, on_delete=models.CASCADE, primary_key=True)
    anger = models.IntegerField()
    anxiety = models.IntegerField()
    embarrassed = models.IntegerField()
    hurt = models.IntegerField()
    neutral = models.IntegerField()
    pleasure = models.IntegerField()
    sad = models.IntegerField()
    
    
    def __str__(self) -> str:
        return self.counseling.customername

    class Meta:
        db_table = 'detected_emotions'
        
    