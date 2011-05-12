from django.conf.urls.defaults import *
from django.conf import settings
from checkapp.profiles.resources.user_profile import UserProfile, \
        UserProfileForm
from checkapp.profiles.resources.user_profiles_list import UserProfilesList

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
    
    # User profiles
    (r'^profiles$',                             UserProfilesList(),),
    (r'^profiles/create$',                      UserProfilesList(),),
    (r'^profiles/new$',                         UserProfileForm(),),
    (r'^profile/(?P<username>[\w-]+)$',         UserProfile(),),
    (r'^profile/(?P<username>[\w-]+)/edit$',    UserProfile(),),
    (r'^profile/(?P<username>[\w-]+)/form$',    UserProfileForm(),),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^files/(?P<path>.*)$',   'django.views.static.serve', \
                {'document_root':   settings.STATIC_DIR}),
        
        (r'^media/(?P<path>.*)$',   'django.views.static.serve', \
                {'document_root':   './media/'}),
    )

