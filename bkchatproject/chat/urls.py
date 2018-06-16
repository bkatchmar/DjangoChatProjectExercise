from django.conf.urls import url
from . import views

app_name = "chat"
urlpatterns = [
    url(r'^my-settings', views.MySettingsView.as_view(), name="my_settings"),
    url(r'^my-rooms', views.MyChatRoomsView.as_view(), name="my_chats"),
    url(r'^all-rooms', views.AllChatRoomsView.as_view(), name="all_chats"),
    url(r'^room/(?P<chat_id>[0-9]+)', views.ChatHomeView.as_view(), name="specific_room"),
    url(r'^', views.ChatHomeView.as_view(), name="home"),
]