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
from checkapp.profiles.models import Application, Category, Platform
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
            messages.warning(self.request, UserMsgs.LIMITED_VIEW)
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
            
            form = {}
            
            if app.owner == guest:
                form['sname'] = self.request.POST.get('app_sname', None)
                form['name'] = self.request.POST.get('app_name', None)
                logo = self.request.FILES.get('logo', None)
                form['cat'] = self.request.POST.get('category', None)
                form['plats'] = self.request.POST.getlist('platform')
                form['devel'] = self.request.POST.get('devel', None)
                form['version'] = self.request.POST.get('version', None)
                form['license'] = self.request.POST.get('license', None)
                form['url'] = self.request.POST.get('url', None)
                form['wiki'] = self.request.POST.get('wiki', None)
                form['blog'] = self.request.POST.get('blog', None)
                form['desc'] = self.request.POST.get('description', None)
                
                try:
                    DataChecker.check_short_name(form['sname'])
                    DataChecker.check_name(form['name'])
                    DataChecker.check_category(form['cat'])
                    
                    if not form['plats']:
                        raise DataError("You have to pick a platform")
                    for i in form['plats']:
                        DataChecker.check_platform(i)
                    
                    if not DataChecker.defined(form['url']):
                        raise DataError("Website cannot be empty")
                    
                    DataChecker.check_url(form['url'])
                    DataChecker.check_url(form['wiki'])
                    DataChecker.check_url(form['blog'])
                    DataChecker.check_description(form['desc'])
                    
                    app.short_name = form['sname']
                    app.name = form['name']
                    app.description = form['desc']
                    app.developer = form['devel']
                    app.version = form['version']
                    app.license = form['license']
                    app.url = form['url']
                    app.wiki = form['wiki']
                    app.blog = form['blog']
                    app.owner = guest
                    
                    category = Category.objects.get(name=form['cat'])
                    app.category = category
                    
                    app.platform.clear()
                    for i in form['plats']:
                        platform = Platform.objects.get(name=i)
                        app.platform.add(platform)
                    
                    if logo is not None:
                        print "logo is not None"
                        app.logo = logo
                    
                    app.save()
                    
                    messages.success(self.request, UserMsgs.APP_EDITED)
                    return HttpResponseRedirect('/app/%s/' % app.short_name)
                except DataError, error:
                    messages.error(self.request, error.msg)
                    
                    categories = Category.objects.all().order_by('name')
                    platforms = Platform.objects.all().order_by('name')
                    
                    return render_to_response('application_form.html', \
                            {'guest': guest, 'app': app, 'form': form, \
                            'cats': categories, 'plats': platforms,}, \
                            context_instance=RequestContext(self.request))
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
                categories = Category.objects.all().order_by('name')
                platforms = Platform.objects.all().order_by('name')
                
                if app.owner == guest:
                    return render_to_response('application_form.html', \
                            {'guest': guest, 'app': app, \
                            'cats': categories, 'plats': platforms,}, \
                            context_instance=RequestContext(self.request))
                else:
                    messages.error(self.request, UserMsgs.FORBIDDEN)
                    return HttpResponseRedirect('/app/%s/' % app.short_name)
            else:
                # Create a new application
                categories = Category.objects.all().order_by('name')
                platforms = Platform.objects.all().order_by('name')
                
                return render_to_response('application_form.html', \
                        {'guest': guest, 'cats': categories, \
                        'plats': platforms,}, \
                        context_instance=RequestContext(self.request))
        else:
            messages.error(self.request, UserMsgs.LOGIN)
            return HttpResponseRedirect('/login/')


