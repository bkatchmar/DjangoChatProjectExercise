from django.conf.urls import url
from . import views

app_name = "chat"
urlpatterns = [
    url(r'^', views.ChatHomeView.as_view(), name="home"),
]