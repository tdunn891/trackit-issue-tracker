from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.view_tickets, name='tickets'),
    url(r'^add_ticket/$', views.add_ticket, name='add_ticket'),
    url(r'^(?P<pk>\d+)/$', views.view_ticket, name='view_ticket'),
    url(r'^edit_ticket/$', views.edit_ticket, name='edit_ticket'),
]
