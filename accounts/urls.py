from django.conf.urls import url
from . import views
from accounts.views import index, logout, login, registration, user_profile, user_list, update_first_name, update_last_name, update_zoomid, grant_staff_access

urlpatterns = [
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', registration, name='registration'),
    url(r'^profile/$', user_profile, name='profile'),
    url(r'^user_list/$', user_list, name='user_list'),
    url(r'^update_first_name/$', update_first_name, name='update_first_name'),
    url(r'^update_last_name/$', update_last_name, name='update_last_name'),
    url(r'^update_zoomid/(?P<pk>\d+)/$', update_zoomid, name='update_zoomid'),
    url(r'^grant_staff_access/(?P<pk>\d+)/$',
        grant_staff_access, name='grant_staff_access')
]
