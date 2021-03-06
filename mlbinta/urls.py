from django.views.generic.simple import redirect_to
from django.conf.urls import patterns, include, url
from haystack.views import SearchView  
from haystack.query import SearchQuerySet  
from content.models import Entry

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

sqs = SearchQuerySet().order_by('title')


urlpatterns = patterns('',
#    (r'^$', 'pages.views.homepage'),
    (r'^$', redirect_to, {'url': '/decay4/'}),
    (r'^old/$', 'pages.views.homepage'),
    (r'^howto/$', 'pages.views.howto'),
    (r'^mission/$', 'pages.views.mission'),
    (r'^privacy/$', 'pages.views.privacy'),
    (r'^search/$', 'pages.views.search'),
    (r'^email/$', 'pages.views.email'),
    (r'^favorites/$', 'pages.views.favorites'),
    (r'^autoclose/$', 'pages.views.autoclose'),
    (r'^splash/$', 'pages.views.splash'),
    (r'^graphtest/$', 'pages.views.graphtest'),
    (r'^autotag/$', 'autotag.views.autotag'),
    (r'^graphtest/(?P<method>[\w]+)/$', 'pages.views.graphtest'),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('userena.urls')),
    (r'^messages/', include('userena.contrib.umessages.urls')),
    (r'^content/', include('content.urls')),
    (r'^(?P<method>[-\w]+)/(?P<tags>[- :.+|\w]+)/$', 'pages.views.taglist'),
    (r'^(?P<method>[-\w]+)/$', 'pages.views.taglist'),
    (r'^learn_submitting/$', 'pages.views.taglist'),
#     url(r'^search/',  
#        SearchView(  
#            searchqueryset=sqs,  
#            ),  
#        name='haystack_search',  
#        ),
    #(r'^search/', include('haystack.urls')),
    # Examples:
    # url(r'^$', 'mlbinta.views.home', name='home'),
    # url(r'^mlbinta/', include('mlbinta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

