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
from checkapp.profiles.models import Application, Category
from checkapp.profiles.helpers.data_checker import DataChecker, DataError
from checkapp.profiles.helpers.user_msgs import UserMsgs

class App(WebResource):
    
    NUM_COMMENTS = 10
    
    def process_GET(self):
        guest = self.request.user
        app = Application.objects.get(short_name = self.appname)
        comments = app.comment_set.order_by('-order').all()[:App.NUM_COMMENTS]
        checkapps = None
        
        if not guest.is_authenticated():
            messages.info(self.request, UserMsgs.LIMITED_VIEW)
        else:
            checkapps = app.checkapp_set.filter(user = guest)
        
        return render_to_response('application.html', \
                {'guest': guest, 'app': app, 'comments': comments,\
                'checkapps': checkapps}, \
                context_instance=RequestContext(self.request)) 
    
    def process_PUT(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            app = Application.objects.get(short_name = self.appname)
            
            if app.owner == guest:
                sname = self.request.POST.get('app_sname', None)
                name = self.request.POST.get('app_name', None)
                logo = self.request.FILES.get('logo', None)
                cat = self.request.POST.get('category', None)
                devel = self.request.POST.get('devel', None)
                version = self.request.POST.get('version', None)
                license = self.request.POST.get('license', None)
                url = self.request.POST.get('url', None)
                desc = self.request.POST.get('desc', None)
                
                try:
                    DataChecker.check_short_name(sname)
                    DataChecker.check_name(name)
                    DataChecker.check_category(cat)
                    DataChecker.check_url(url)
                    
                    app.short_name = sname
                    app.name = name
                    app.description = desc
                    app.developer = devel
                    app.version = version
                    app.license = license
                    app.url = url
                    app.owner = guest
                    
                    category = Category.objects.get(name=cat)
                    app.category = category
                    
                    if logo is not None:
                        print "logo is not None"
                        app.logo = logo
                    
                    app.save()
                    
                    messages.success(self.request, UserMsgs.APP_EDITED)
                    return HttpResponseRedirect('/app/%s/' % app.short_name)
                except DataError as error:
                    messages.info(self.request, UserMsgs.FORM_ERROR)
                    messages.error(self.request, error.msg)
                    return HttpResponseRedirect('/app/%s/form/' % \
                            app.short_name)
            else:
                messages.error(self.request, UserMsgs.FORBIDDEN)
                return HttpResponseRedirect('/app/%s/' % app.short_name)
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')
    

class AppForm(WebResource):
    
    def process_GET(self):
        guest = self.request.user
        
        if guest.is_authenticated():
            if self.appname:
                # Edit an application
                app = Application.objects.get(short_name = self.appname)
                categories = Category.objects.all()
                
                if app.owner == guest:
                    return render_to_response('application_form.html', \
                            {'guest': guest, 'app': app, \
                            'cats': categories,}, \
                            context_instance=RequestContext(self.request))
                else:
                    messages.error(self.request, UserMsgs.FORBIDDEN)
                    return HttpResponseRedirect('/app/%s/' % app.short_name)
            else:
                # Create a new application
                categories = Category.objects.all()
                
                return render_to_response('application_form.html', \
                        {'guest': guest, 'cats': categories,}, \
                        context_instance=RequestContext(self.request))
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')


