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
from checkapp.profiles.models import Profile
from checkapp.profiles.helpers.data_checker import DataChecker, DataError
from checkapp.profiles.helpers.user_msgs import UserMsgs

class UserProfilesList(WebResource):
    
    USERS_PER_PAGE = 10
    
    def process_GET(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            uname = self.request.GET.get('username', "")
            fname = self.request.GET.get('first_name', "")
            lname = self.request.GET.get('last_name', "")
            email = self.request.GET.get('email', "")
            
            user_list = Profile.objects.order_by('first_name', 'last_name', \
                    'username').exclude(username=guest.username)
            search = {}
            
            if uname != "":
                user_list = user_list.filter(username__icontains = uname)
                search['username'] = uname
            
            if fname != "":
                user_list = user_list.filter(first_name__icontains = fname)
                search['first_name'] = fname
            
            if lname != "":
                user_list = user_list.filter(last_name__icontains = lname)
                search['last_name'] = lname
            
            if email != "":
                user_list = user_list.filter(email = email)
                search['email'] = email
            
            users = self.paginate_results(user_list, \
                    UserProfilesList.USERS_PER_PAGE)
            
            return render_to_response('profiles_list.html', \
                    {'guest': guest, 'users': users, 'search': search,}, \
                    context_instance=RequestContext(self.request))
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')
    
    def process_POST(self):
        form = {}
        form['uname'] = self.request.POST.get('username', None)
        form['fname'] = self.request.POST.get('first_name', None)
        form['lname'] = self.request.POST.get('last_name', None)
        form['email'] = self.request.POST.get('email', None)
        picture = self.request.FILES.get('pic', None)
        password = self.request.POST.get('password', None)
        cpassword = self.request.POST.get('cpassword', None)
        
        try:
            DataChecker.check_username(form['uname'])
            DataChecker.user_exists(form['uname'])
            DataChecker.check_first_name(form['fname'])
            DataChecker.check_last_name(form['lname'])
            DataChecker.check_email(form['email'])
            DataChecker.check_password(password, cpassword)
            
            user = Profile()
            user.username = form['uname']
            user.first_name = form['fname']
            user.last_name = form['lname']
            user.email = form['email']
            user.set_password(password)
            
            if picture:
                user.pic = picture
            
            user.save()
            
            # User is logged in without typing again its data
            user = authenticate(username=form['uname'], password=password)
            login(self.request, user)
            
            messages.success(self.request, UserMsgs.USER_CREATED)
            return HttpResponseRedirect('/profile/%s/' % user.username)
        except DataError, error:
            messages.error(self.request, error.msg)
            
            return render_to_response('profile_creation_form.html', \
                    {'form': form,}, \
                    context_instance=RequestContext(self.request))

