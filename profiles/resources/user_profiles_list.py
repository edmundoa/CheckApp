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
from checkapp.profiles.resources.web_resource import WebResource
from checkapp.profiles.models import Profile

class UserProfilesList(WebResource):
    
    USERS_PER_PAGE = 10
    
    def process_GET(self):
        uname = self.request.GET.get('username', "")
        fname = self.request.GET.get('first_name', "")
        lname = self.request.GET.get('last_name', "")
        email = self.request.GET.get('email', "")
        index = int(self.request.GET.get('index', 0))
        findex = index + UserProfilesList.USERS_PER_PAGE
        
        users = Profile.objects.all()
        search = {}
        
        if uname != "":
            users = users.filter(username__icontains=uname)
            search['username'] = uname
        
        if fname != "":
            users = users.filter(first_name__icontains=fname)
            search['first_name'] = fname
        
        if lname != "":
            users = users.filter(last_name__icontains=lname)
            search['last_name'] = lname
        
        if email != "":
            users = users.filter(email=email)
            search['email'] = email
        
        search['index'] = findex
        
        if len(users) < findex:
            search['last_result'] = True
        
        users[index:findex]
        
        return render_to_response('profiles_list.html', {'users': users, 'search': search})
    
    def process_POST(self):
        uname = self.request.POST.get('username', None)
        fname = self.request.POST.get('first_name', None)
        lname = self.request.POST.get('last_name', None)
        email = self.request.POST.get('email', None)
        picture = self.request.FILES.get('pic', None)
        
        password = self.request.POST.get('password', None)
        cpassword = self.request.POST.get('cpassword', None)
        
        if (uname is None) or (uname == ""):
            raise Exception
        
        users = Profile.objects.filter(username=uname)
        if (users):
            raise Exception
        
        if (email is None) or (email == ""):
            raise Exception
        
        if (password is None) or (password == ""):
            raise Exception
        
        if (password != cpassword):
            raise Exception
        
        user = Profile()
        user.username = uname
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.pic = picture
        user.password = password
        user.save ()
        
        return HttpResponseRedirect('/profile/%s' % uname)

