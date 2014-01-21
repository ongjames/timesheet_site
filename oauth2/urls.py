from django.conf.urls import patterns, url
from oauth2 import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^oauth2callback/', views.callback, name='callback'),
        )