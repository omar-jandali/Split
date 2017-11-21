from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.groups_home, name='groups'),
    url(r'^create/$', views.create_group, name='create_group'),
]
