from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/video/$', consumers.VideoConsumer.as_asgi()),
    re_path(r'ws/video/(?P<counseling_id>\d+)/$', consumers.VideoConsumer.as_asgi()),
]