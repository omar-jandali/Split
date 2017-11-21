from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.groups_home, name='groups'),
    url(r'^create/$', views.create_group, name='create_group'),
    url(r'^(?P<groupid>[0-9]+)/(?P<groupname>[\w+-]+)/$', views.group_home, name='group_home'),
]
