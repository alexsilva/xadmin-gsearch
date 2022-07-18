# coding=utf-8
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from xadmin.filters import SEARCH_VAR
from xadmin.plugins.utils import get_context_dict
from xadmin.views import CommAdminView, ListAdminView
from xplugin_gsearch.search import search


class GlobalSearchView(CommAdminView):
	template_name = "gsearch/search.html"
	search_title = "Resultados da busca"

	def get_search_view(self, model_option):
		return self.get_view(ListAdminView, model_option)

	def block_nav_form(self, context, nodes):
		context = get_context_dict(context or {})
		nodes.append(render_to_string("gsearch/blocks/search.nav.form.html",
		                              context=context))

	def get(self, request, **kwargs):
		context = self.get_context()
		views = []
		count = 0
		search_val = request.GET.get(SEARCH_VAR, '')
		for model in search:
			opts = self.admin_site.get_registry(model)
			model_option = search.get_option(model, opts)
			search_view = self.get_search_view(model_option)
			query_string = search_view.get_query_string({
				SEARCH_VAR: search_val
			})
			views.append({
				'view': search_view,
				'url': search_view.model_admin_url("changelist") + query_string
			})
			count += search_view.get_total()
		context['gsearch'] = {
			'url': self.get_admin_url("gsearch"),
			'title': self.search_title,
			'search_param': SEARCH_VAR,
			'search_val': search_val,
			'count': count,
			'views': views
		}
		response = TemplateResponse(
			request,
			self.template_name,
			context=context
		)
		return response
