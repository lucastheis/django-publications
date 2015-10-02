__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django import forms
from django.forms import widgets
from django.db import models

class PagesWidget(widgets.MultiWidget):
	def __init__(self, *args, **kwargs):
		attrs = {'style': 'width: 40px; text-align: center;'}
		forms.widgets.MultiWidget.__init__(self,
			[widgets.TextInput(attrs), widgets.TextInput(attrs)], *args, **kwargs)


	def format_output(self, rendered_widgets):
		to = ' <span style="vertical-align: middle;">to</span> '
		return rendered_widgets[0] + to + rendered_widgets[1]


	def decompress(self, value):
		if value:
			values = value.split('-')

			if len(values) > 1:
				return values
			if len(values) > 0:
				return [values[0], values[0]]
		return [None, None]


class PagesForm(forms.MultiValueField):
	widget = PagesWidget

	def __init__(self, *args, **kwargs):
		forms.MultiValueField.__init__(self, [
			forms.CharField(),
			forms.CharField()], *args, **kwargs)


	def compress(self, data_list):
		if data_list:
			if data_list[0] and data_list[1]:
				if data_list[0] == data_list[1]:
					return str(data_list[0])
				return str(data_list[0]) + '-' + str(data_list[1])
			if data_list[0]:
				return str(data_list[0])
			if data_list[1]:
				return str(data_list[1])
		return ''


class PagesField(models.Field):
	def formfield(self, **kwargs):
		kwargs['form_class'] = PagesForm
		return models.Field.formfield(self, **kwargs)


	def get_internal_type(self):
		return 'CharField'

try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ["^publications\.fields\.PagesField"])
except:
	pass
