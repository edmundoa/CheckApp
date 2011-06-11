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
from checkapp.profiles.models import Application, Comment
from checkapp.profiles.helpers.data_checker import DataChecker, DataError
from checkapp.profiles.helpers.user_msgs import UserMsgs

class Comment_(WebResource):
    
    def process_GET(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            app = Application.objects.get(short_name = self.appname)
            comment = Comment.objects.get(app = app, order = self.commentno)
            
            return render_to_response('comment.html', \
                    {'guest': guest, 'app': app, \
                    'comment': comment, 'edit': False,}, \
                    context_instance=RequestContext(self.request))
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')
    
    def process_PUT(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            app = Application.objects.get(short_name = self.appname)
            comment = Comment.objects.get(app = app, order = self.commentno)
            
            try:
                text = self.request.POST.get('text', '')
                
                DataChecker.check_comment(text)
                
                comment.text = text
                comment.save()
                
                return HttpResponseRedirect('/app/%s/comment/%s/' % \
                        (app.short_name, comment.order))
            except DataError as error:
                messages.error(self.request, error.msg)
                
                return render_to_response('comment.html', \
                        {'guest': guest, 'app': app, \
                        'comment': comment, 'edit': True, 'text': text,}, \
                        context_instance=RequestContext(self.request))
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')


class CommentForm(WebResource):
    
    def process_GET(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            app = Application.objects.get(short_name = self.appname)
            comment = Comment.objects.get(app = app, order = self.commentno)
            
            if guest == comment.user:
                return render_to_response('comment.html', \
                        {'guest': guest, 'app': app, \
                        'comment': comment, 'edit': True,}, \
                        context_instance=RequestContext(self.request))
            else:
                messages.error(self.request, UserMsgs.FORBIDDEN)
                return HttpResponseRedirect('/profile/%s/' % guest.username)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')


