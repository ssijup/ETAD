from django.urls import re_path

from . import consumers
# def sam():
#     print('Entered websocket_urlpatterns')
websocket_urlpatterns = [

    re_path(r"ws/chat/(?P<id>\d+)/$", consumers.PersonChatConsumer.as_asgi()),


]