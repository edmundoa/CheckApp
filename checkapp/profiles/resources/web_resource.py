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

from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator, InvalidPage, EmptyPage

class WebResource:
    def __call__(self, request, _method='', appname='', username='', \
            commentno='', friend=''):
        method = request.method
        
        try:
            method_param = request.REQUEST['_method']
            method_param = method_param.upper()
            if method_param in ['GET', 'POST', 'PUT', 'DELETE']:
                method = method_param
        except KeyError:
            pass
        
        try:
            callback = getattr(self, 'process_%s' % method)
        except AttributeError:
            return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
        
        self.request = request
        
        self.appname = appname
        self.username = username
        self.commentno = commentno
        self.friend = friend
        
        return callback()
    
    
    def paginate_results(self, result_list, max_per_page):
        paginator = Paginator(result_list, max_per_page)
        
        try:
            page = int(self.request.REQUEST.get('page', '1'))
        except:
            page = 1
        
        try:
            results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            results = paginator.page(paginator.num_pages)
        
        return results


