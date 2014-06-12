__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from .orderedmodeladmin import OrderedModelAdmin

class TypeAdmin(OrderedModelAdmin):
	list_display = ('type', 'description', 'hidden', 'move_up_down_links')
