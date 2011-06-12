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

import re
from checkapp.profiles.models import Application, Category, CheckApp, \
        Comment, Platform, Profile


class DataError(Exception):
    
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return repr(self.msg)
    
    def __unicode__(self):
        return repr(self.msg)


class DataChecker:
    
    TEXT_RE = re.compile('[\w\d\-\.]+')
    EMAIL_RE = re.compile('[\w\-\.]+@[\w\-]+\.[\w\.]{2,}')
    URL_RE = re.compile('http(s)?:\/\/(\.)*')
    
    @staticmethod
    def defined(string):
        return (string is not None) and (string != "")
    
    @staticmethod
    def user_exists(uname):
        user = Profile.objects.filter(username=uname)
        if len(user) > 0:
            raise DataError('User already exists')
    
    @staticmethod
    def check_username(uname):
        if not DataChecker.defined(uname):
            raise DataError("Username cannot be empty")
        
        if len(uname) < 3:
            raise DataError('Username must have at least 3 characters')
        
        if not DataChecker.TEXT_RE.match(uname):
            raise DataError("Invalid username format")
    
    @staticmethod
    def check_first_name(fname):
        if not DataChecker.defined(fname):
            raise DataError("First name cannot be empty")
    
    @staticmethod
    def check_last_name(lname):
        if not DataChecker.defined(lname):
            raise DataError("Last name cannot be empty")
    
    @staticmethod
    def check_email(email):
        if not DataChecker.defined(email):
            raise DataError("E-Mail cannot be empty")
        
        if not DataChecker.EMAIL_RE.match(email):
            raise DataError("Invalid E-Mail format")
    
    @staticmethod
    def check_password(password, confirmation):
        if not DataChecker.defined(password):
            raise DataError("Password cannot be empty")
        
        if len(password) < 6:
            raise DataError("Password has to have at least 6 characters")
        
        if (password != confirmation):
            raise DataError("Passwords don't match")
    
    @staticmethod
    def check_short_name(sname):
        if not DataChecker.defined(sname):
            raise DataError("Short name cannot be empty")
        
        if len(sname) < 3:
            raise DataError('Short name must have at least 3 characters')
        
        if not DataChecker.TEXT_RE.match(sname):
            raise DataError("Invalid short name format")
    
    @staticmethod
    def check_name(name):
        if not DataChecker.defined(name):
            raise DataError("Name cannot be empty")
    
    @staticmethod
    def check_category(category):
        try:
            Category.objects.get(name=category)
        except:
            raise DataError("Category '%s' doesn't exist" % category)
    
    @staticmethod
    def check_platform(platform):
        try:
            Platform.objects.get(name=platform)
        except:
            raise DataError("Platform '%s' doesn't exist" % platform)
    
    @staticmethod
    def check_url(url):
        if not DataChecker.defined(url):
           return 
        
        if not DataChecker.URL_RE.match(url):
            raise DataError("%s is not a valid URL" % url)
    
    @staticmethod
    def check_comment(comment):
        if not DataChecker.defined(comment):
            raise DataError("Comment cannot be empty")
        
        if len(comment) > Comment.COMMENT_LENGTH:
            raise DataError("Comment is too long (max. %s characters)" %\
                    (Comment.COMMENT_LENGTH))
    
    @staticmethod
    def check_ca_comment(ca_comment):
        if len(ca_comment) > CheckApp.COMMENT_LENGTH:
            raise DataError("Comment is too long (max. %s characters)" %\
                    (CheckApp.COMMENT_LENGTH))
    
    @staticmethod
    def check_description(description):
        if not DataChecker.defined(description):
            raise DataError("Description cannot be empty")
        
        if len(description) > Application.DESC_LENGTH:
            raise DataError("Description is too long (max. %s characters)" %\
                    (Application.DESC_LENGTH))


