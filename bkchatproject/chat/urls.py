from django.conf.urls import url
from . import views

app_name = "chat"
urlpatterns = [
    url(r'^all-rooms', views.AllChatRoomsView.as_view(), name="all_chats"),
    url(r'^room/(?P<contract_id>[0-9]+)', views.ChatHomeView.as_view(), name="specific_room"),
    url(r'^', views.ChatHomeView.as_view(), name="home"),
]