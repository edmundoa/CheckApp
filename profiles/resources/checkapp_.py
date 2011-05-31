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
from checkapp.profiles.models import Application, Profile, CheckApp
from checkapp.profiles.helpers.data_checker import DataChecker, DataError
from checkapp.profiles.helpers.user_msgs import UserMsgs
from datetime import date

class CheckApp_(WebResource):
    
    CHECKAPPS_NUMBER = 5
    
    def process_GET(self):
        guest = Profile.objects.get(username = self.username)
        
        if guest.is_authenticated():
            app = Application.objects.get(short_name = self.appname)
            today = date.today()
            checkapps_no = guest.checkapp_set.filter(user = guest, \
                    time__year = today.year, time__month = today.month, \
                    time__day = today.day).count()
            
            if checkapps_no <= CheckApp_.CHECKAPPS_NUMBER:
                last_checkapp = guest.checkapp_set.all().order_by('-time')[0]
                return render_to_response('checkapp_confirm.html', \
                        {'guest': guest, 'app': app, 'ca_no': checkapps_no, \
                        'last_ca': last_checkapp,}, \
                        context_instance=RequestContext(self.request))
            else:
                messages.info(self.request, UserMsgs.CHECKAPPS_EXCEEDED)
                return HttpResponseRedirect('/app/%s/' % app.short_name)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')
    
    def process_PUT(self):
        guest = Profile.objects.get(username = self.username)
        
        if guest.is_authenticated():
            app = Application.objects.get(short_name = self.appname)
            today = date.today()
            checkapps_no = guest.checkapp_set.filter(user = guest, \
                    time__year = today.year, time__month = today.month, \
                    time__day = today.day).count()
            
            if checkapps_no <= CheckApp_.CHECKAPPS_NUMBER:
                text = self.request.POST.get('comment', '')
                
                checkapp = CheckApp()
                checkapp.user = guest
                checkapp.app = app
                checkapp.text = text
                checkapp.save()
                
                messages.success(self.request, UserMsgs.CHECKAPP_DONE)
                return HttpResponseRedirect('/app/%s/' % app.short_name)
            else:
                messages.info(self.request, UserMsgs.CHECKAPPS_EXCEEDED)
                return HttpResponseRedirect('/app/%s/' % app.short_name)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')

