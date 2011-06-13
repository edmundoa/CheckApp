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

from checkapp.profiles.models import Pin, Merit

class MeritsChecker:
    
    @staticmethod
    def check_total(user, cat, sumup):
        '''Check merits related to passed category'''
        retval = False
        
        if sumup == Pin.GRADES[cat][Pin.ZERO_GRADE]:
            pin = Pin.objects.get(category = cat, grade = Pin.ZERO_GRADE)
            retval = True
        elif sumup == Pin.GRADES[cat][Pin.FIRST_GRADE]:
            pin = Pin.objects.get(category = cat, grade = Pin.FIRST_GRADE)
            retval = True
        elif sumup == Pin.GRADES[cat][Pin.SECOND_GRADE]:
            pin = Pin.objects.get(category = cat, grade = Pin.SECOND_GRADE)
            retval = True
        elif sumup == Pin.GRADES[cat][Pin.THIRD_GRADE]:
            pin = Pin.objects.get(category = cat, grade = Pin.THIRD_GRADE)
            retval = True
        
        if retval:
            merit = Merit()
            merit.user = user
            merit.pin = pin
            merit.save()
        
        return retval
    
    @staticmethod
    def check_checkapps(user):
        ca_no = user.checkapp_set.count()
        return MeritsChecker.check_total(user, Pin.TOTAL_CHECKAPPS_CAT, ca_no)
    
    @staticmethod
    def check_comments(user):
        com_no = user.comment_set.count()
        return MeritsChecker.check_total(user, Pin.TOTAL_COMMENTS_CAT, com_no)


