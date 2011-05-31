from django.conf.urls.defaults import *
from django.conf import settings
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


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^checkapp/', include('checkapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/',    include(admin.site.urls)),
    
    (r'^$', 'django.views.generic.simple.redirect_to',  {'url': '/login'}),
    
    # Session management
    (r'^login/$',   Login(),),
    (r'^logout/$',  Logout(),),
    
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
    (r'^profile/(?P<username>[\w-]+)/notifications/$',  NotificationsList(),),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^files/(?P<path>.*)$',   'django.views.static.serve', \
                {'document_root':   settings.STATIC_DIR}),
        (r'^media/(?P<path>.*)$',   'django.views.static.serve', \
                {'document_root':   './media/', 'show_indexes': True,}),
    )

