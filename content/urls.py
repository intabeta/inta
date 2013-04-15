from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from content import views as content_views
#from userena import settings as userena_settings

urlpatterns = patterns('',
    # Signup, signin and signout
    url(r'^myig/$',
       content_views.myig,
       name='content_myig'),
       
    url(r'^ig/(?P<slug>[-\w]+)/(?P<method>[-\w]+)/$',
       content_views.ig_list,
       name='content_ig_list'),
    url(r'^ig/$',
       content_views.ig,
       name='content_ig'),
       
    url(r'^tags/(?P<method>[-\w]+)/(?P<tags>[- |\w]+)/$',
    	content_views.tag_list,
    	name='content_tag_list'),
       
       
    url(r'^ig_proposal/$',
       content_views.ig_proposal,
       name='content_ig_proposal'),
    url(r'^ig_proposal_done/$',
       content_views.ig_proposal_done,
       name='content_ig_proposal_done'),
       
    url(r'^submit/$',
       content_views.submit,
       name='content_submit'),
    url(r'^submit_plugin/$',
       content_views.submit_plugin,
       name='content_submit_plugin'),
       
    url(r'^submit_details/$',
       content_views.submit_details,
       name='content_submit_details'),
       
#     url(r'^signin/$',
#        userena_views.signin,
#        name='userena_signin'),
#     url(r'^signout/$',
#        userena_views.signout,
#        name='userena_signout'),
# 
#     # Reset password
#     url(r'^password/reset/$',
#        auth_views.password_reset,
#        {'template_name': 'userena/password_reset_form.html',
#         'email_template_name': 'userena/emails/password_reset_message.txt'},
#        name='userena_password_reset'),
#     url(r'^password/reset/done/$',
#        auth_views.password_reset_done,
#        {'template_name': 'userena/password_reset_done.html'},
#        name='userena_password_reset_done'),
#     url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
#        auth_views.password_reset_confirm,
#        {'template_name': 'userena/password_reset_confirm_form.html'},
#        name='userena_password_reset_confirm'),
#     url(r'^password/reset/confirm/complete/$',
#        auth_views.password_reset_complete,
#        {'template_name': 'userena/password_reset_complete.html'}),
# 
#     # Signup
#     url(r'^(?P<username>[\.\w]+)/signup/complete/$',
#        userena_views.direct_to_user_template,
#        {'template_name': 'userena/signup_complete.html',
#         'extra_context': {'userena_activation_required': userena_settings.USERENA_ACTIVATION_REQUIRED,
#                           'userena_activation_days': userena_settings.USERENA_ACTIVATION_DAYS}},
#        name='userena_signup_complete'),
# 
#     # Activate
#     url(r'^(?P<username>[\.\w]+)/activate/(?P<activation_key>\w+)/$',
#        userena_views.activate,
#        name='userena_activate'),
# 
#     # Change email and confirm it
#     url(r'^(?P<username>[\.\w]+)/email/$',
#        userena_views.email_change,
#        name='userena_email_change'),
#     url(r'^(?P<username>[\.\w]+)/email/complete/$',
#        userena_views.direct_to_user_template,
#        {'template_name': 'userena/email_change_complete.html'},
#        name='userena_email_change_complete'),
#     url(r'^(?P<username>[\.\w]+)/confirm-email/complete/$',
#        userena_views.direct_to_user_template,
#        {'template_name': 'userena/email_confirm_complete.html'},
#        name='userena_email_confirm_complete'),
#     url(r'^(?P<username>[\.\w]+)/confirm-email/(?P<confirmation_key>\w+)/$',
#        userena_views.email_confirm,
#        name='userena_email_confirm'),
# 
#     # Disabled account
#     url(r'^(?P<username>[\.\w]+)/disabled/$',
#        userena_views.direct_to_user_template,
#        {'template_name': 'userena/disabled.html'},
#        name='userena_disabled'),
# 
#     # Change password
#     url(r'^(?P<username>[\.\w]+)/password/$',
#        userena_views.password_change,
#        name='userena_password_change'),
#     url(r'^(?P<username>[\.\w]+)/password/complete/$',
#        userena_views.direct_to_user_template,
#        {'template_name': 'userena/password_complete.html'},
#        name='userena_password_change_complete'),
# 
#     # Edit profile
#     url(r'^(?P<username>[\.\w]+)/edit/$',
#        userena_views.profile_edit,
#        name='userena_profile_edit'),
# 
#     # View profiles
#     url(r'^(?P<username>(?!signout|signup|signin)[\.\w]+)/$',
#        userena_views.profile_detail,
#        name='userena_profile_detail'),
#     url(r'^page/(?P<page>[0-9]+)/$',
#        userena_views.ProfileListView.as_view(),
#        name='userena_profile_list_paginated'),
#     url(r'^$',
#        userena_views.ProfileListView.as_view(),
#        name='userena_profile_list'),
)
