from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.accounts, name='accounts'),
    url(r'^link_login/$', views.link_login, name='link_login'),
    url(r'^link_routing/$', views.link_routing, name='link_routing'),
]
