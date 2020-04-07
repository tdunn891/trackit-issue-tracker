from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tickets', views.RestView)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', views.view_tickets, name='tickets'),
    url(r'^kanban/$', views.kanban, name='kanban'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^change_status/(?P<pk>\d+)/(?P<new_status>[a-zA-Z_ ]+)/$',
        views.change_status, name='change_status'),
    url(r'^add_ticket/$', views.add_ticket, name='add_ticket'),
    url(r'^(?P<pk>\d+)/$', views.view_ticket, name='view_ticket'),
    url(r'^upvote/(?P<pk>\d+)/$', views.upvote, name='upvote'),
    url(r'^edit_ticket/(?P<pk>\d+)/$', views.edit_ticket, name='edit_ticket'),
]
