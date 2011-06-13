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

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from checkapp.profiles.resources.web_resource import WebResource
from checkapp.profiles.models import Profile, Notification
from checkapp.profiles.helpers.data_checker import DataChecker, DataError
from checkapp.profiles.helpers.user_msgs import UserMsgs

class NotificationsList(WebResource):
    
    MAX_NOTIFICATIONS = 15
    
    def process_GET(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            if guest.username == self.username:
                notifications = guest.notification_set.order_by('-time').all()
                new_nots = [i for i in notifications if i.read == False]
                readed_nots = [i for i in notifications if i.read == True]
                
                no_new_nots = len(new_nots)
                
                if no_new_nots >= NotificationsList.MAX_NOTIFICATIONS:
                    try:
                        readed_nots = [readed_nots[0]]
                    except:
                        readed_nots = []
                else:
                    max_readed = NotificationsList.MAX_NOTIFICATIONS - \
                            no_new_nots
                    readed_nots = readed_nots[:max_readed]
                
                for i in new_nots:
                    i.mark_read()
                
                return render_to_response('notifications.html', \
                        {'guest': guest, 'new_nots': new_nots, \
                        'readed_nots': readed_nots,}, \
                        context_instance=RequestContext(self.request))
            else:
                messages.error(self.request, UserMsgs.FORBIDDEN)
                return HttpResponseRedirect('/profile/%s/' % guest.username)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')


