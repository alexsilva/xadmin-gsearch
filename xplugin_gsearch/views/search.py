# coding=utf-8
from django.template.response import TemplateResponse
from xadmin.views import CommAdminView
from xplugin_gsearch.search import search


class GlobalSearchView(CommAdminView):
	template_name = "gsearch/search.html"

	def get(self, request, **kwargs):
		context = self.get_context()
		context['gsearch'] = search
		response = TemplateResponse(
			request,
			self.template_name,
			context=context
		)
		return response
