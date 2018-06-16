from django.conf.urls import url
from . import views

app_name = "chat"
urlpatterns = [
    url(r'^api/edit-message/(?P<mesage_id>[0-9]+)', views.JsonEditMessage.as_view(), name='json_edit_message'),
    url(r'^api/like-message/(?P<mesage_id>[0-9]+)', views.JsonLikeMessage.as_view(), name='json_like_message'),
    url(r'^my-liked-messages', views.MyLikedMessages.as_view(), name="my_liked_messages"),
    url(r'^my-settings', views.MySettingsView.as_view(), name="my_settings"),
    url(r'^my-rooms', views.MyChatRoomsView.as_view(), name="my_chats"),
    url(r'^all-rooms', views.AllChatRoomsView.as_view(), name="all_chats"),
    url(r'^room/(?P<chat_id>[0-9]+)', views.ChatHomeView.as_view(), name="specific_room"),
    url(r'^', views.ChatHomeView.as_view(), name="home"),
]