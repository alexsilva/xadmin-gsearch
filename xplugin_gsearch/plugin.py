# coding=utf-8
from django.template.loader import render_to_string
from xadmin.filters import SEARCH_VAR
from xadmin.plugins.utils import get_context_dict
from xadmin.views import ListAdminView
from xadmin.views.base import BaseAdminPlugin
from xplugin_gsearch.views.search import GlobalSearchView


class GlobalSearchPlugin(BaseAdminPlugin):
	global_search_template = "gsearch/blocks/search.nav.top.html"

	def init_request(self, *args, **kwargs):
		return not isinstance(self.admin_view, (GlobalSearchView, ListAdminView))

	def setup(self, *args, **kwargs):
		self.search_url = self.admin_view.get_admin_url("gsearch")

	def block_top_navmenu(self, context, nodes):
		context = get_context_dict(context or {})
		context['gsearch'] = {
			'url': self.search_url,
			'param': SEARCH_VAR,
			'val': self.request.GET.get(SEARCH_VAR, '')
		}
		nodes.append(
			render_to_string(self.global_search_template,
			                 context=context)
		)

	block_top_navmenu.priority = 1000
