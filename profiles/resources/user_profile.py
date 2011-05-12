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
from checkapp.profiles.resources.web_resource import WebResource
from checkapp.profiles.models import Profile

class UserProfile(WebResource):
    
    def process_GET(self):
        user = Profile.objects.get(username = self.username)
        return render_to_response('profile.html', {'user': user,})
    
    def process_PUT(self):
        fname = self.request.POST.get('first_name', None)
        lname = self.request.POST.get('last_name', None)
        email = self.request.POST.get('email', None)
        picture = self.request.FILES.get('pic', None)
        
        password = self.request.POST.get('password', None)
        cpassword = self.request.POST.get('cpassword', None)
        
        user = Profile.objects.get(username = self.username)
        user.first_name = fname
        user.last_name = lname
        
        if (email is not None) and (email != ""):
            print "email: %s" % email
            user.email = email
        
        if picture is not None:
            print "picture is not None"
            user.pic = picture
        
        if (password is not None) and (password != ""):
            print "password: %s" % password
            if password == cpassword:
                print "changing password"
                user.password = password
        
        user.save()
        
        return HttpResponseRedirect('/profile/%s' % self.username)


class UserProfileForm(WebResource):
    
    def process_GET(self):
        try:
            user = Profile.objects.get(username = self.username)
            
            return render_to_response('profile_form.html', {'user': user,}, \
                    context_instance=RequestContext(self.request))
        except:
            return render_to_response('profile_form.html', {'user': None,}, \
                    context_instance=RequestContext(self.request))

