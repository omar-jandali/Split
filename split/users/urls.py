from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.user_home, name='home'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^signup/$', views.user_signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^personal/$', views.verify_personal, name='personal'),
    url(r'^business/$', views.verify_business, name='business'),
    url(r'^search/$', views.search_user, name="searched"),
    url(r'^(?P<username>[\w+]+)/$', views.user_profile, name='user_profile'),
    url(r'^(?P<username>[\w+]+)/request/$', views.send_request, name='send_request'),
    url(r'^(?P<username>[\w+]+)/accept/$', views.accept_request, name='accept_request'),
    url(r'^(?P<username>[\w+]+)/decline/$', views.decline_request, name='decline_request'),
]
