from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from profiles.models import *

class UserProfileInline(admin.StackedInline):
    model = Profile

class ProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

#    list_display = ('pic', 'friends', 'pins')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notification)
admin.site.register(Application)
admin.site.register(Category)
admin.site.register(Screenshot)
admin.site.register(CheckApp)
admin.site.register(Comment)
admin.site.register(Merit)
admin.site.register(Pin)

