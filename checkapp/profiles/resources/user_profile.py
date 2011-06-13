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
from checkapp.profiles.models import Profile, Merit
from checkapp.profiles.helpers.data_checker import DataChecker, DataError
from checkapp.profiles.helpers.user_msgs import UserMsgs

class UserProfile(WebResource):
    
    NUM_FRIENDS = 5
    NUM_CHECKAPPS = 5
    NUM_COMMENTS = 5
    NUM_MERITS = 5
    
    def process_GET(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            host = Profile.objects.get(username = self.username)
            friends = host.friends.all().order_by('?') \
                    [:UserProfile.NUM_FRIENDS]
            checkapps = host.checkapp_set.all().order_by('-time') \
                    [:UserProfile.NUM_CHECKAPPS]
            comments = host.comment_set.all().order_by('-time') \
                    [:UserProfile.NUM_COMMENTS]
            merits = Merit.objects.filter(user=host).order_by('?')\
                    [:UserProfile.NUM_MERITS]
            
            return render_to_response('profile.html', \
                    {'guest': guest, 'host': host, 'friends': friends, \
                    'checkapps': checkapps, 'comments': comments, \
                    'merits': merits,}, \
                    context_instance=RequestContext(self.request))
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')
    
    def process_PUT(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            if guest.username == self.username:
                form = {}
                form['fname'] = self.request.POST.get('first_name', None)
                form['lname'] = self.request.POST.get('last_name', None)
                form['email'] = self.request.POST.get('email', None)
                picture = self.request.FILES.get('pic', None)
                password = self.request.POST.get('password', None)
                cpassword = self.request.POST.get('cpassword', None)
                
                try:
                    DataChecker.check_first_name(form['fname'])
                    DataChecker.check_last_name(form['lname'])
                    DataChecker.check_email(form['email'])
                    
                    guest.first_name = form['fname']
                    guest.last_name = form['lname']
                    guest.email = form['email']
                    
                    if picture is not None:
                        print "picture is not None"
                        guest.pic = picture
                    
                    if DataChecker.defined(password):
                        print "password: %s" % password
                        DataChecker.check_password(password, \
                                cpassword)
                        guest.set_password(password)
                    
                    guest.save()
                    
                    messages.success(self.request, UserMsgs.USER_EDITED)
                    return HttpResponseRedirect('/profile/%s/' % self.username)
                except DataError, error:
                    messages.error(self.request, error.msg)
                    
                    return render_to_response('profile_edit_form.html', \
                            {'guest': guest, 'form': form,}, \
                            context_instance=RequestContext(self.request))
            else:
                return HttpResponseRedirect('/profile/%s/' % self.username)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')


class UserProfileForm(WebResource):
    
    def process_GET(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            if guest.username == self.username:
                return render_to_response('profile_edit_form.html', \
                        {'guest': guest,}, \
                        context_instance=RequestContext(self.request))
            else:
                return HttpResponseRedirect('/profile/%s/' % self.username)
        else:
            return render_to_response('profile_creation_form.html', \
                    context_instance=RequestContext(self.request))

