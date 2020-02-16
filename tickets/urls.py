from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.view_tickets, name='tickets'),
    url(r'^add_ticket/$', views.add_ticket, name='add_ticket'),
]
