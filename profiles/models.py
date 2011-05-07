# coding=utf8
#
# Copyright (C) 2011  Edmundo Álvarez Jiménez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Edmundo Álvarez Jiménez <e.alvarezj@gmail.com>


from django.db import models
from django.contrib.auth.models import User, UserManager

# Create your models here.
class Profile(User):
    '''Represents a user of the application'''
    friends = models.ManyToManyField("self", symmetrical=False, \
            verbose_name="Friends of a user")
    pins = models.ManyToManyField("Pin", through="Merit", \
            verbose_name="Pins a user has won")
    
    def __unicode__(self):
        return unicode(User)


class Notification(models.Model):
    '''Represents a notification message for a user'''
    user = models.ForeignKey("Profile", verbose_name="User to be notified")
    text = models.CharField(max_length=500, \
            verbose_name="Notification message")
    url = models.URLField(null=True, verbose_name="Notification URL")
    time = models.DateTimeField(auto_now_add=True, \
            verbose_name="Time when notification raised")
    read = models.BooleanField(default=False, \
            verbose_name="Indicates whether a notification has been read")
    
    def __unicode__(self):
        return (("'%s' to %s on %s") % (text, user.name, time))


class Application(models.Model):
    '''Represents an application available for check up'''
    name = models.CharField(max_length=50, unique=True, \
            verbose_name="Application name")
    logo = models.ImageField(upload_to="app_logos/%Y%m%d", null=True, \
            height_field=500, width_field=500, \
            verbose_name="Path to application logo")
    description = models.CharField(max_length=500, \
            verbose_name="Application description")
    vendor = models.CharField(max_length=50, null=True, \
            verbose_name="Application distributor")
    developers = models.CharField(max_length=200, null=True, \
            verbose_name="Name of application developers")
    url = models.URLField(verbose_name="Application URL")
    owner = models.ForeignKey("Profile", null=True, \
            verbose_name="Application administrator")
    category = models.ForeignKey("Category", \
            verbose_name="Application category")
    
    def __unicode__(self):
        return (("Application %s on %s") % (name, category.name))


class Category(models.Model):
    '''Represents a category of applications'''
    name = models.CharField(max_length=100, unique=True, \
            verbose_name="Category name")
    
    def __unicode__(self):
        return (("Category %s") % (name))


class Screenshot(models.Model):
    '''Represents a screenshot of an application'''
    description = models.CharField(max_length=200, null=True, \
            verbose_name="Screenshot description")
    app = models.ForeignKey("Application", \
            verbose_name="Application which has been captured")
    image = models.ImageField(upload_to="app_screenshots/%Y%m%d", \
            height_field=2000, width_field=2000, \
            verbose_name="Path to application screenshot")
    
    def __unicode__(self):
        return (("Screenshot of %s on '%s'") % (app.name, image))


class CheckApp(models.Model):
    '''Represents a check up of an application'''
    user = models.ForeignKey("Profile", \
            verbose_name="User who has checked up")
    app = models.ForeignKey("Application", \
            verbose_name="Application checked up")
    text = models.CharField(max_length=500, null=True, \
            verbose_name="Message for the check up")
    time = models.DateTimeField(auto_now_add=True, \
            verbose_name="Time of check up")
    
    def __unicode__(self):
        return (("%s has checked app %s on %s") % (user.username, \
                app.name, time))


class Comment(models.Model):
    '''Represents a comment on an application profile'''
    user = models.ForeignKey("Profile", verbose_name="User who has commented")
    app = models.ForeignKey("Application", verbose_name="Application commented")
    text = models.CharField(max_length=500, verbose_name="Commented text")
    time = models.DateTimeField(auto_now_add=True, \
            verbose_name="Time when user commented")
    
    def __unicode__(self):
        return (("%s has commented on %s") % (user.name, app.name))


class Reply(models.Model):
    '''Represents a reply to a comment'''
    user = models.ForeignKey("Profile", verbose_name="User who has commented")
    comment = models.ForeignKey("Comment", verbose_name="Comment replied")
    text = models.CharField(max_length=500, verbose_name="Commented text")
    time = models.DateTimeField(auto_now_add=True, \
            verbose_name="Time when user commented")
    
    def __unicode__(self):
        return (("%s has replied to %s") % (user.name, comment.id))


class Merit(models.Model):
    '''Represents a merit achieved, gained by checking up'''
    user = models.ForeignKey("Profile", \
            verbose_name="User who achieved a merit")
    pin = models.ForeignKey("Pin", verbose_name="Pin won")
    app = models.ForeignKey("Application", verbose_name="Related application")
    time = models.DateTimeField(auto_now_add=True, \
            verbose_name="Time of merit achievement")
    
    def __unicode__(self):
        return (("%s won %s on %s") % (user.name, pin.name, time))


class Pin(models.Model):
    '''Represents a kind of price for the user'''
    name = models.CharField(max_length=50, verbose_name="Pin name")
    text = models.CharField(max_length=100, verbose_name="Pin text")
    image = models.ImageField(upload_to="pins", \
            verbose_name="Path to pin image")
    
    def __unicode__(self):
        return (("Pin %s") % (name))


