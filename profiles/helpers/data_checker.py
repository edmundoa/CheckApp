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

from checkapp.profiles.models import Profile, Category


class DataError(Exception):
    
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return repr(self.msg)
    
    def __unicode__(self):
        return repr(self.msg)


class DataChecker:
    
    @staticmethod
    def defined(string):
        return (string is not None) or (string != "")
    
    @staticmethod
    def user_exists(uname):
        user = Profile.objects.filter(username=uname)
        if len(user) > 0:
            raise DataError('User already exists')
    
    @staticmethod
    def check_username(uname):
        if not DataChecker.defined(uname):
            raise DataError("Username cannot be empty")
    
    @staticmethod
    def check_first_name(fname):
        if not DataChecker.defined(fname):
            raise DataError("First name cannot be empty")
    
    @staticmethod
    def check_email(email):
        if not DataChecker.defined(email):
            raise DataError("E-Mail cannot be empty")
    
    @staticmethod
    def check_password(password, confirmation):
        if not DataChecker.defined(password):
            raise DataError("Password cannot be empty")
        
        if (password != confirmation):
            raise DataError("Passwords don't match")
    
    @staticmethod
    def check_short_name(sname):
        if not DataChecker.defined(sname):
            raise DataError("Short name cannot be empty")
    
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
    def check_url(url):
        if DataChecker.defined(url):
            pass


