"""
Copyright (c) 2009, Ben Firshman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * The names of its contributors may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.util import unquote
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.functional import update_wrapper

class OrderedModelAdmin(admin.ModelAdmin):
	def get_urls(self):
		from django.conf.urls.defaults import patterns, url
		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.admin_site.admin_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)
		info = self.model._meta.app_label, self.model._meta.module_name
		return patterns('',
			url(r'^(.+)/move-(up)/$',
				wrap(self.move_view),
				name='%s_%s_move_up' % info),
			url(r'^(.+)/move-(down)/$',
				wrap(self.move_view),
				name='%s_%s_move_down' % info),
		) + super(OrderedModelAdmin, self).get_urls()

	def move_view(self, request, object_id, direction):
		obj = get_object_or_404(self.model, pk=unquote(object_id))
		if direction == 'up':
			obj.move_up()
		else:
			obj.move_down()
		return HttpResponseRedirect('../../')

	def move_up_down_links(self, obj):
		return '<a href="../../%(app_label)s/%(module_name)s/%(object_id)s/move-up/"><img src="%(ADMIN_MEDIA_PREFIX)simg/admin/arrow-up.gif" alt="Move up" /></a> <a href="../../%(app_label)s/%(module_name)s/%(object_id)s/move-down/"><img src="%(ADMIN_MEDIA_PREFIX)simg/admin/arrow-down.gif" alt="Move up" /></a>' % {
			'app_label': self.model._meta.app_label,
			'module_name': self.model._meta.module_name,
			'object_id': obj.id,
			'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX,
		}
	move_up_down_links.allow_tags = True
	move_up_down_links.short_description = 'Move'
