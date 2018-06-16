from django.conf.urls import include, url
from django.contrib import admin
from accounts.views import AccountLoginView

urlpatterns = [
    url(r'^$', AccountLoginView.as_view(), name='index'),
    url(r'^account/', include('accounts.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^admin/', admin.site.urls)
]