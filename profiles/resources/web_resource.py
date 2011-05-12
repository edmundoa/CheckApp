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

class WebResource:
    def __call__(self, request, _method='', username=''):
        method = request.method
        
        try:
            method_param = request.REQUEST['_method']
            method_param = method_param.upper()
            if method_param in ['PUT', 'DELETE']:
                method = method_param
        except KeyError:
            pass
        
        try:
            callback = getattr(self, 'process_%s' % method)
        except AttributeError:
            return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
        
        self.request = request
        
        self.username = username
        
        return callback()

