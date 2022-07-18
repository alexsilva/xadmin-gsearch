# coding=utf-8
from django.template.response import TemplateResponse
from xadmin.views import CommAdminView, ListAdminView
from xplugin_gsearch.search import search


class GlobalSearchView(CommAdminView):
	template_name = "gsearch/search.html"

	def get_search_view(self, model_option):
		return self.get_view(ListAdminView, model_option)

	def get(self, request, **kwargs):
		context = self.get_context()
		views = []
		count = 0
		for model in search:
			opts = self.admin_site.get_registry(model)
			model_option = search.get_option(model, opts)
			search_view = self.get_search_view(model_option)
			query_string = search_view.get_query_string()
			views.append({
				'view': search_view,
				'url': search_view.model_admin_url("changelist") + query_string
			})
			count += search_view.get_total()
		context['gsearch'] = {
			'url': self.get_admin_url("gsearch"),
			'count': count,
			'views': views
		}
		response = TemplateResponse(
			request,
			self.template_name,
			context=context
		)
		return response
