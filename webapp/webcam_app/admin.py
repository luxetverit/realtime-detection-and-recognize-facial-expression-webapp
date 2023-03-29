from django.contrib import admin
from .models import Counseling,DetectedEmotions

# Register your models here.
admin.site.register(Counseling)
admin.site.register(DetectedEmotions)