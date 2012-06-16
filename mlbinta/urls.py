from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'pages.views.homepage'),
    (r'^howto/$', 'pages.views.howto'),
    (r'^mission/$', 'pages.views.mission'),
    (r'^privacy/$', 'pages.views.privacy'),
    (r'^autoclose/$', 'pages.views.autoclose'),
    
    (r'^accounts/', include('userena.urls')),
    (r'^messages/', include('userena.contrib.umessages.urls')),
    (r'^content/', include('content.urls')),
    # Examples:
    # url(r'^$', 'mlbinta.views.home', name='home'),
    # url(r'^mlbinta/', include('mlbinta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
