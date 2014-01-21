from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timesheet_site_v2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'timesheet.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('users.urls')),
    url(r'^timesheet/', include('timesheet.urls')),
    url(r'^oauth2/', include('oauth2.urls')),
)
