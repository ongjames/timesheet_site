from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
        url(r'^$', views.login, name='users_index'),
        url(r'^login/', views.login, name='users_login'),
        url(r'^logout/', views.logout, name='users_logout'),
        url(r'^register/', views.register, name='users_register'),
        url(r'^profile/', views.profile, name='users_profile'),
        url(r'^pm/', views.pm, name='users_pm'),
        url(r'^resetpw/', views.resetpw, name='users_resetpw'),
        )