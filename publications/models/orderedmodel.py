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

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

class OrderedModel(models.Model):
	"""
	An abstract model that allows objects to be ordered relative to each other.
	Provides an ``order`` field.
	"""

	order = models.PositiveIntegerField(editable=False)

	class Meta:
		abstract = True
		ordering = ('order',)


	def save(self, *args, **kwargs):
		if not self.id:
			qs = self.__class__.objects.order_by('-order')
			try:
				self.order = qs[0].order + 1
			except IndexError:
				self.order = 0
		super(OrderedModel, self).save(*args, **kwargs)


	def _move(self, up):
		qs = self.__class__._default_manager
		if up:
			qs = qs.order_by('-order').filter(order__lt=self.order)
		else:
			qs = qs.filter(order__gt=self.order)
		try:
			replacement = qs[0]
		except IndexError:
			# already first/last
			return
		self.order, replacement.order = replacement.order, self.order
		self.save()
		replacement.save()


	def move_down(self):
		"""
		Move this object down one position.
		"""
		return self._move(up=False)


	def move_up(self):
		"""
		Move this object up one position.
		"""
		return self._move(up=True)
