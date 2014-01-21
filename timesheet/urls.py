from django.conf.urls import patterns, url
from timesheet import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='timesheet_index'),
        url(r'^json', views.index_json, name='timesheet_index_json'),
        url(r'^about/', views.about, name='timesheet_about'),
        url(r'^new_entry/', views.newEntry, name='timesheet_new_entry'),
        url(r'^entry/(?P<entry_url>\w+)/$', views.entry, name='timesheet_entry'),
        url(r'^test_data/', views.test_data, name='timesheet_test_data'),
        )