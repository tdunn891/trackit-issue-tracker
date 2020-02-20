from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.view_tickets, name='tickets'),
    url(r'^add_ticket/$', views.add_ticket, name='add_ticket'),
    url(r'^(?P<pk>\d+)/$', views.view_ticket, name='view_ticket'),
    url(r'^edit_ticket/(?P<pk>\d+)/$', views.edit_ticket, name='edit_ticket'),
    url(r'^cancel_ticket/(?P<pk>\d+)/$',
        views.cancel_ticket, name='cancel_ticket'),
    url(r'^delete_ticket/(?P<pk>\d+)/$',
        views.delete_ticket, name='delete_ticket'),
    # url(r'^add_comment/$', views.add_comment, name='add_comment'),
    # url(r'^add_comment/(?P<pk>\d+)/$', views.add_comment, name='add_comment'),
]
