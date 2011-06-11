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
import threading

# Create your models here.
class Profile(User):
    '''Represents a user of the application'''
    pic = models.ImageField(upload_to="user_pics/%Y%m%d", blank=True, \
            null=True, verbose_name="Path to user picture")
    friends = models.ManyToManyField("self", blank=True, symmetrical=False, \
            verbose_name="Friends of a user")
    pins = models.ManyToManyField("Pin", blank=True, through="Merit", \
            verbose_name="Pins a user has won")
    
    def count_unread(self):
        return self.notification_set.filter(read=False).count()
    
    def last_checkapp(self):
        try:
            return self.checkapp_set.order_by('-time')[0]
        except:
            return None
    
    def __unicode__(self):
        return ("%s") % (self.username)


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
    
    def mark_read(self):
        self.read = True
        self.save()
    
    def __unicode__(self):
        return (("'%s' to %s on %s") % (self.text, self.user.username, \
                self.time))


class Application(models.Model):
    '''Represents an application available for check up'''
    
    DESC_LENGTH = 300
    
    short_name = models.CharField(max_length=30, unique=True, \
            verbose_name="Application short name")
    name = models.CharField(max_length=100, unique=True, \
            verbose_name="Application name")
    logo = models.ImageField(upload_to="app_logos/%Y%m%d", blank=True, \
            null=True, verbose_name="Path to application logo")
    description = models.CharField(max_length=DESC_LENGTH, \
            verbose_name="Application description")
    version = models.CharField(max_length=20, null=True, \
            verbose_name="Latest application version")
    developer = models.CharField(max_length=200, null=True, \
            verbose_name="Name of application developers")
    license = models.CharField(max_length=50, null=True, \
            verbose_name="Application license")
    url = models.URLField(verbose_name="Application URL")
    wiki = models.URLField(null=True, verbose_name="Application Wiki")
    blog = models.URLField(null=True, verbose_name="Application blog")
    twitter = models.CharField(max_length=150, null=True, \
            verbose_name="Twitter profile")
    facebook = models.CharField(max_length=150, null=True, \
            verbose_name="FB profile")
    owner = models.ForeignKey("Profile", blank=True, null=True, \
            related_name="owner", \
            verbose_name="Application administrator")
    superuser = models.ForeignKey("Profile", blank=True, null=True, \
            related_name="superuser", \
            verbose_name="Application superuser")
    category = models.ForeignKey("Category", \
            verbose_name="Application category")
    platform = models.ManyToManyField("Platform", \
            verbose_name="Supported platforms")
    
    def __unicode__(self):
        return (("Application %s on %s") % (self.name, self.category.name))


class Category(models.Model):
    '''Represents a category of applications'''
    name = models.CharField(max_length=100, unique=True, \
            verbose_name="Category name")
    
    def __unicode__(self):
        return (("%s") % (self.name))


class Platform(models.Model):
    '''Represents a platform where an application runs'''
    name = models.CharField(max_length=100, unique=True, \
            verbose_name="Platform name")
    
    def __unicode__(self):
        return (("%s") % (self.name))


class Screenshot(models.Model):
    '''Represents a screenshot of an application'''
    description = models.CharField(max_length=200, null=True, \
            verbose_name="Screenshot description")
    app = models.ForeignKey("Application", \
            verbose_name="Application which has been captured")
    image = models.ImageField(upload_to="app_screenshots/%Y%m%d", \
            verbose_name="Path to application screenshot")
    
    def __unicode__(self):
        return (("Screenshot of %s on '%s'") % (self.app.name, self.image))


class CheckApp(models.Model):
    '''Represents a check up of an application'''
    
    COMMENT_LENGTH = 140
    
    user = models.ForeignKey("Profile", \
            verbose_name="User who has checked up")
    app = models.ForeignKey("Application", \
            verbose_name="Application checked up")
    text = models.CharField(max_length=COMMENT_LENGTH, null=True, \
            verbose_name="Message for the check up")
    time = models.DateTimeField(auto_now_add=True, \
            verbose_name="Time of check up")
    
    def __unicode__(self):
        return (("%s has checked app %s on %s") % (self.user.username, \
                self.app.name, self.time))


class Comment(models.Model):
    '''Represents a comment on an application profile'''
    
    COMMENT_LENGTH = 2048
    
    order = models.IntegerField(verbose_name="Application's number of comment")
    user = models.ForeignKey("Profile", verbose_name="User who has commented")
    app = models.ForeignKey("Application", verbose_name="Application commented")
    text = models.CharField(max_length=COMMENT_LENGTH, \
            verbose_name="Commented text")
    time = models.DateTimeField(auto_now_add=True, \
            verbose_name="Time when user commented")
    
    def save(self, *args, **kwargs):
        lock = threading.Lock()
        lock.acquire()
        
        try:
            if not self.id:
                try:
                    comment = self.app.comment_set.order_by('-order').all()[0]
                    self.order = comment.order + 1
                except IndexError:
                    self.order = 1
            super(Comment, self).save(*args, **kwargs)
        finally:
            lock.release()
    
    def __unicode__(self):
        return (("%s, %s on %s") % (self.order, self.user.username, \
                self.app.name))


class Merit(models.Model):
    '''Represents a merit achieved, gained by checking up'''
    user = models.ForeignKey("Profile", \
            verbose_name="User who achieved a merit")
    pin = models.ForeignKey("Pin", verbose_name="Pin won")
    time = models.DateTimeField(auto_now_add=True, \
            verbose_name="Time of merit achievement")
    
    def __unicode__(self):
        return (("%s won %s on %s") % (self.user.username, self.pin.name, \
                self.time))


class Pin(models.Model):
    '''Represents a kind of price for the user'''
    
    GRADES = (
        (0, 1, 2,  3,   4,),   # Number of grades
        (1, 1, 10, 100, 500,),
        (2, 1, 10, 50,  100,),
    )
    
    TOTAL_CHECKAPPS_CAT = GRADES[1][0]
    TOTAL_COMMENTS_CAT = GRADES[2][0]
    
    ZERO_GRADE = GRADES[0][1]
    FIRST_GRADE = GRADES[0][2]
    SECOND_GRADE = GRADES[0][3]
    THIRD_GRADE = GRADES[0][4]
    
    name = models.CharField(max_length=50, verbose_name="Pin name")
    text = models.CharField(max_length=100, verbose_name="Pin text")
    image = models.ImageField(upload_to="pins", \
            verbose_name="Path to pin image")
    category = models.IntegerField(verbose_name="Pin category")
    grade = models.IntegerField(verbose_name="Level of pin")
    
    def __unicode__(self):
        return (("%s") % (self.name))


