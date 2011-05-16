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
from checkapp.profiles.models import Profile
from checkapp.profiles.helpers.user_msgs import UserMsgs

class FriendsList(WebResource):
    
    def process_GET(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            if guest.username == self.username:
                return render_to_response('friends_list.html', \
                        {'guest': guest,})
            else:
                return HttpResponseRedirect('/profile/%s/' % self.username)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')
        
    def process_POST(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            friend = Profile.objects.get(username = self.friend)
            guest.friends.add(friend)
            guest.save()
            
            return HttpResponseRedirect('/profile/%s/friends/' % guest.username)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')
    
    def process_DELETE(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            friend = Profile.objects.get(username = self.friend)
            guest.friends.remove(friend)
            guest.save()
            
            messages.success(self.request, UserMsgs.FRIEND_REMOVED)
            return HttpResponseRedirect('/profile/%s/friends/' % guest.username)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')

