from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.groups_home, name='groups'),
    url(r'^create/$', views.create_group, name='create_group'),
    url(r'^(?P<groupid>[\w+-]+)/leave_group/$',
        views.leave_group, name='leave_group'),
    url(r'^(?P<groupid>[0-9]+)/(?P<groupname>[\w+-]+)/$',
        views.group_home, name='group_home'),
    url(r'^(?P<groupid>[0-9]+)/(?P<groupname>[\w+-]+)/create_expense/$',
        views.create_expense, name='create_expense'),
    url(r'^(?P<groupid>[0-9]+)/(?P<groupname>[\w+-]+)/create_bundle/$',
        views.create_bundle, name='create_bundle'),
    url(r'^(?P<expensename>[\w+-]+)/(?P<reference>[0-9]+)/even_expense/$',
        views.even_expense, name='even_expense'),
    url(r'^(?P<expensename>[\w+-]+)/(?P<reference>[0-9]+)/individual_expense/$',
        views.individual_expense, name='individual_expense'),
    url(r'^(?P<expenseid>[\w+-]+)/(?P<activityid>[0-9]+)/verify/$',
        views.verify_expense, name='verify_expense'),
    url(r'^(?P<bundleid>[\w+-]+)/(?P<activityid>[0-9]+)/verify_bundle/$',
        views.verify_bundle, name='verify_bundle'),
    url(r'^(?P<groupid>[\w+-]+)/(?P<memberid>[0-9]+)/set_host/$',
        views.set_host, name='set_host'),
]
