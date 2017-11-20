from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.groups_home, name='groups'),
]
