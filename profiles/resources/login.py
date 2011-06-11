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
from django.contrib.auth import authenticate, login
from django.contrib import messages
from checkapp.profiles.resources.web_resource import WebResource
from checkapp.profiles.helpers.user_msgs import UserMsgs

class Login(WebResource):
    
    def process_GET(self):
        user = self.request.user
        
        if user.is_authenticated():
            return HttpResponseRedirect('/profile/%s/' % user.username)
        else:
            return render_to_response('index.html', \
                    context_instance=RequestContext(self.request))
    
    def process_PUT(self):
        username = self.request.POST.get('username', None)
        password = self.request.POST.get('password', None)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect('/profile/%s/' % user.username)
            else:
                # Return a 'disabled account' error message
                messages.error(self.request, UserMsgs.DISABLED_ACCOUNT)
                return HttpResponseRedirect('/login/')
        else:
            # Login error
            messages.error(self.request, UserMsgs.LOGIN_ERROR)
            return HttpResponseRedirect('/login/')

