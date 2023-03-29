from django.contrib import admin

from .models import Counseling,DetectedEmotions,Videos

# Register your models here.
admin.site.register(Counseling)
admin.site.register(DetectedEmotions)
admin.site.register(Videos)

