from django.contrib import admin
from .models import BoardPost, BoardComment # 현재 경로의 models.py 안에 있는 Post를 가져다 쓰겠음 


# Register your models here.
admin.site.register(BoardPost)
admin.site.register(BoardComment)