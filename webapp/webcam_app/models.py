from django.db import models

from django.contrib.auth import authenticate

from account.models import User
from django.db import models


class Counseling(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True) #상담자
    customername =models.CharField(max_length=20) # 상담받는 고객
    counsel_subject=models.CharField(max_length=50) # 상담주제 
    content=models.TextField() # 상담내용 

    realtime_true_false=models.BooleanField(default=False)
    storage_data = models.FileField(upload_to="cam/", blank=True)  
    download_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    

    
    
    def __str__(self): #상담자 
        return '비워둠'+'의고객'+self.customername+'pk'+str(self.pk)
    

    
    def save(self, *args, **kwargs):
        # 첫 번째로 Counseling 모델을 저장합니다.
        super(Counseling, self).save(*args, **kwargs)
        if not hasattr(self, 'detectedemotions'):
            detected_emotions = DetectedEmotions(counseling_id=self.pk)
            detected_emotions.save()

    
    class Meta:
        db_table = 'counseling'
        
    
class Videos(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid', to_field='userid')
    original_video_url = models.CharField(max_length=2083)
    processed_video_url = models.CharField(max_length=2083, blank=True, null=True)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed=False
        db_table = 'videos'

    
class DetectedEmotions(models.Model):
    counseling = models.OneToOneField(Counseling, on_delete=models.CASCADE, primary_key=True)
    anger = models.IntegerField(blank=True, null=True)
    anxiety = models.IntegerField(blank=True, null=True)
    embarrassed = models.IntegerField(blank=True, null=True)
    hurt = models.IntegerField(blank=True, null=True)
    neutral = models.IntegerField(blank=True, null=True)
    pleasure = models.IntegerField(blank=True, null=True)
    sad = models.IntegerField(blank=True, null=True)
    
    
    def __str__(self):
        return 'pk:'+str(self.pk)+'와'+self.counseling.customername

    class Meta:
        db_table = 'detected_emotions'
        
