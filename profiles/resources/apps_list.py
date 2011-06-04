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
from checkapp.profiles.models import Application, Category, Profile
from checkapp.profiles.helpers.data_checker import DataChecker, DataError
from checkapp.profiles.helpers.user_msgs import UserMsgs

class AppsList(WebResource):
    
    APPS_PER_PAGE = 10
    
    def process_GET(self):
        guest = self.request.user
        
        if self.username:
            # List user applications
            if guest.is_authenticated():
                if guest.username == self.username:
                    apps = guest.owner.all().order_by('name')
                    categories = Category.objects.all()
                    
                    return render_to_response('apps_list.html', \
                            {'guest': guest, 'apps': apps, \
                            'cats': categories, 'user': True,}, \
                            context_instance=RequestContext(self.request))
                else:
                    messages.error(self.request, UserMsgs.FORBIDDEN)
                    return HttpResponseRedirect('/apps/')
            else:
                messages.error(self.request, UserMsgs.LOGIN)
                return HttpResponseRedirect('/login/')
        else:
            # List all applications
            appname = self.request.GET.get('name', "")
            developer = self.request.GET.get('developer', "")
            license = self.request.GET.get('license', "")
            catname = self.request.GET.get('category', "")
            
            apps = Application.objects.all().order_by('name')
            search = {}
            
            if appname != "":
                apps = apps.filter(name__icontains = appname)
                search['name'] = appname
            
            if developer != "":
                apps = apps.filter(developer__icontains = developer)
                search['developer'] = appname
            
            if license != "":
                apps = apps.filter(license__icontains = license)
                search['name'] = appname
            
            if catname != "":
                cat = Category.objects.get(name = catname)
                apps = apps.filter(category = cat)
                search['category'] = catname
            
            categories = Category.objects.all()
            
            return render_to_response('apps_list.html', \
                    {'guest': guest, 'apps': apps, 'cats': categories, \
                    'search': search, 'user': False,}, \
                    context_instance=RequestContext(self.request))
    
    def process_POST(self):
        guest = self.request.user
        
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
            
            app = Application()
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
                app.logo = logo
            
            app.save()
            
            messages.success(self.request, UserMsgs.APP_ADDED)
            return HttpResponseRedirect('/app/%s/' % app.short_name)
        except DataError as error:
            messages.warning(self.request, UserMsgs.FORM_ERROR)
            messages.error(self.request, error.msg)
            return HttpResponseRedirect('/apps/new/')


