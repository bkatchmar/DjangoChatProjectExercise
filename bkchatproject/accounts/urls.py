from django.conf.urls import url
from . import views

app_name = "accounts"
urlpatterns = [
    url(r'^account-create/', views.AccountCreationView.as_view(), name='account_create'),
]