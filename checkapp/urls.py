from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import redirect_to_login, password_reset, \
        password_reset_done, password_reset_confirm, password_reset_complete
from checkapp.profiles.resources.login import Login
from checkapp.profiles.resources.logout import Logout
from checkapp.profiles.resources.app import App, \
        AppForm
from checkapp.profiles.resources.apps_list import AppsList
from checkapp.profiles.resources.user_profile import UserProfile, \
        UserProfileForm
from checkapp.profiles.resources.user_profiles_list import UserProfilesList
from checkapp.profiles.resources.friends_list import FriendsList
from checkapp.profiles.resources.notifications_list import NotificationsList
from checkapp.profiles.resources.comment import Comment_, CommentForm
from checkapp.profiles.resources.comments_list import CommentsList
from checkapp.profiles.resources.checkapp_ import CheckApp_
from checkapp.profiles.resources.checkapps_list import CheckAppsList
from checkapp.profiles.resources.merits_list import MeritsList
from checkapp.profiles.resources.about import About
from checkapp.profiles.resources.contact import Contact


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'checkapp.profiles.views.view_404'
handler500 = 'checkapp.profiles.views.view_500'

urlpatterns = patterns('',
    # Example:
    # (r'^checkapp/', include('checkapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/',    include(admin.site.urls)),
    
    (r'^$', 'django.views.generic.simple.redirect_to',  {'url': '/login/',}),
    
    # CheckApp information
    (r'^about/$',   About(),),
    (r'^contact/$', Contact(),),
    
    # Session management
    (r'^login/$',   Login(),),
    (r'^logout/$',  Logout(),),
    (r'^redirect/$', redirect_to_login, {'login_url': '/login/'}),
    (r'^reset/$', password_reset, {'template_name': 'reset.html', \
            'email_template_name': 'email_template.html',}),
    (r'^reset/done/$', password_reset_done, \
            {'template_name': 'reset_done.html',}),
    (r'^reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', \
            password_reset_confirm, {'template_name': 'reset_confirm.html',}),
    (r'^reset/complete/$', password_reset_complete, \
            {'template_name': 'reset_complete.html',}),
    
    # Applications
    (r'^apps/$',    AppsList(),),
    (r'^apps/create/$', AppsList(),),
    (r'^apps/new/$',    AppForm(),),
    (r'^app/(?P<appname>[\w-]+)/$', App(),),
    (r'^app/(?P<appname>[\w-]+)/comment/(?P<commentno>[\d-]+)/$',\
            Comment_(),),
    (r'^app/(?P<appname>[\w-]+)/comment/(?P<commentno>[\d-]+)/edit/$',\
            Comment_(),),
    (r'^app/(?P<appname>[\w-]+)/comment/(?P<commentno>[\d-]+)/form/$',\
            CommentForm(),),
    (r'^app/(?P<appname>[\w-]+)/comments/$',    CommentsList(),),
    (r'^app/(?P<appname>[\w-]+)/comments/create/$', CommentsList(),),
    (r'^app/(?P<appname>[\w-]+)/edit/$',    App(),),
    (r'^app/(?P<appname>[\w-]+)/form/$',    AppForm(),),
    
    # User profiles
    (r'^profiles/$',    UserProfilesList(),),
    (r'^profiles/create/$', UserProfilesList(),),
    (r'^profiles/new/$',    UserProfileForm(),),
    (r'^profile/(?P<username>[\w-]+)/$',    UserProfile(),),
    (r'^profile/(?P<username>[\w-]+)/apps/$',   AppsList(),),
    (r'^profile/(?P<username>[\w-]+)/checkapp/(?P<appname>[\w-]+)/$',\
            CheckApp_(),),
    (r'^profile/(?P<username>[\w-]+)/checkapp/(?P<appname>[\w-]+)/create/$',\
            CheckApp_(),),
    (r'^profile/(?P<username>[\w-]+)/checkapps/$',  CheckAppsList(),),
    (r'^profile/(?P<username>[\w-]+)/comments/$',   CommentsList(),),
    (r'^profile/(?P<username>[\w-]+)/edit/$',   UserProfile(),),
    (r'^profile/(?P<username>[\w-]+)/form/$',   UserProfileForm(),),
    (r'^profile/(?P<username>[\w-]+)/friends/$',    FriendsList(),),
    (r'^profile/(?P<username>[\w-]+)/friends/(?P<friend>[\w-]+)/add/$',  \
            FriendsList(),),
    (r'^profile/(?P<username>[\w-]+)/friends/(?P<friend>[\w-]+)/del/$',  \
            FriendsList(),),
    (r'^profile/(?P<username>[\w-]+)/merits/$',   MeritsList(),),
    (r'^profile/(?P<username>[\w-]+)/notifications/$',  NotificationsList(),),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^files/(?P<path>.*)$',   'django.views.static.serve', \
                {'document_root':   settings.STATIC_DIR}),
        (r'^media/(?P<path>.*)$',   'django.views.static.serve', \
                {'document_root':   './media/', 'show_indexes': True,}),
    )

