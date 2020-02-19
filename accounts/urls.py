from django.conf.urls import url, include
from . import views
from accounts.views import index, logout, login, registration, user_profile, user_list

urlpatterns = [
    # url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', registration, name='registration'),
    url(r'^profile/$', user_profile, name='profile'),
    url(r'^user_list/$', user_list, name='user_list'),
]
