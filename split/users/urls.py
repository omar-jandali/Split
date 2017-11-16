from django.conf.urls import url
from . import views, method

urlpatterns = [
    url(r'^$', views.user_home, name='home'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^signup/$', views.user_signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^personal/$', views.verify_personal, name='personal'),
    url(r'^business/$', views.verify_business, name='business'),
    url(r'^test/$', method.test, name='test'),
]
