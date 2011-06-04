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
from checkapp.profiles.models import Application, Profile, Comment
from checkapp.profiles.helpers.data_checker import DataChecker, DataError
from checkapp.profiles.helpers.user_msgs import UserMsgs
from checkapp.profiles.helpers.merits_checker import MeritsChecker

class CommentsList(WebResource):
    
    def process_GET(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            if self.appname:
                # Show comments of an application
                app = Application.objects.get(short_name = self.appname)
                comments = app.comment_set.all().order_by('-time')
                
                return render_to_response('app_comments_list.html', \
                        {'guest': guest, 'app': app, \
                        'comments': comments,}, \
                        context_instance=RequestContext(self.request))
            else:
                # Show comments of a user
                host = Profile.objects.get(username = self.username)
                comments = host.comment_set.all().order_by('-time')
                
                return render_to_response('profile_comments_list.html', \
                        {'guest': guest, 'host': host, \
                        'comments': comments,}, \
                        context_instance=RequestContext(self.request))
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')
        
    def process_POST(self):
        guest = self.request.user
        
        text = self.request.POST.get('text', None)
        
        if guest.is_authenticated():
            try:
                app = Application.objects.get(short_name = self.appname)
                comment = Comment()
                comment.user = guest
                comment.app = app
                comment.text = text
                comment.save()
                
                messages.success(self.request, UserMsgs.COMMENT_ADDED)
                
                if MeritsChecker.check_comments(guest):
                    messages.info(self.request, UserMsgs.MERIT_ACHIEVED)
                
                return HttpResponseRedirect('/app/%s/comments/' % \
                        app.short_name)
            except:
                messages.error(self.request, UserMsgs.UNEXPECTED_ERROR)
                return HttpResponseRedirect('/profile/%s/' % guest.username)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')


