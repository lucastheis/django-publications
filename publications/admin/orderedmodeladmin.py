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

from functools import update_wrapper

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib import admin
try:
    from django.contrib.admin.utils import unquote
except ImportError:
    # Django <= 1.6
    from django.contrib.admin.util import unquote
from django.contrib.admin.views.main import ChangeList
from django.db.models.options import Options

# Django <= 1.6
if not getattr(Options, 'model_name', False):
    Options.model_name = lambda self: self.module_name.lower()
if not getattr(ChangeList, 'get_queryset', False):
    ChangeList.get_queryset = ChangeList.get_query_set

class OrderedModelAdmin(admin.ModelAdmin):

    def get_model_info(self):
        return dict(app=self.model._meta.app_label,
                    model=self.model._meta.model_name)

    def get_urls(self):
        try:
            from django.conf.urls import url
        except ImportError:
            from django.conf.urls.defaults import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        return [
            url(r'^(.+)/move-(up)/$', wrap(self.move_view),
                name='{app}_{model}_order_up'.format(**self.get_model_info())),
            url(r'^(.+)/move-(down)/$', wrap(self.move_view),
                name='{app}_{model}_order_down'.format(**self.get_model_info())),
        ] + super(OrderedModelAdmin, self).get_urls()

    def _get_changelist(self, request):
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)

        cl = ChangeList(request, self.model, list_display,
                        list_display_links, self.list_filter, self.date_hierarchy,
                        self.search_fields, self.list_select_related,
                        self.list_per_page, self.list_max_show_all, self.list_editable,
                        self, sortable_by=self.list_display)

        return cl

    request_query_string = ''

    def changelist_view(self, request, extra_context=None):
        cl = self._get_changelist(request)
        self.request_query_string = cl.get_query_string()
        return super(OrderedModelAdmin, self).changelist_view(request, extra_context)

    def move_view(self, request, object_id, direction):
        cl = self._get_changelist(request)
        qs = cl.get_queryset(request)

        obj = get_object_or_404(self.model, pk=unquote(object_id))
        obj.move(direction, qs)

        return HttpResponseRedirect('../../%s' % self.request_query_string)

    def move_up_down_links(self, obj):
        return render_to_string("admin/publications/order_controls.html", {
            'app_label': self.model._meta.app_label,
            'module_name': self.model._meta.model_name,
            'object_id': obj.id,
            'urls': {
                'up': reverse("admin:{app}_{model}_order_up".format(**self.get_model_info()), args=[obj.id, 'up']),
                'down': reverse("admin:{app}_{model}_order_down".format(**self.get_model_info()), args=[obj.id, 'down']),
            },
            'query_string': self.request_query_string
        })
    move_up_down_links.allow_tags = True
    move_up_down_links.short_description = _(u'Move')
