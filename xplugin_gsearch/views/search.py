# coding=utf-8
import django.forms as django_forms
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.functional import cached_property
from xadmin.filters import SEARCH_VAR
from xadmin.plugins.utils import get_context_dict
from xadmin.views import CommAdminView, ListAdminView
from xplugin_gsearch.search import search


class SearchForm(django_forms.Form):
	models = django_forms.MultipleChoiceField(required=False)

	def get_val(self, field_name):
		return (self.cleaned_data[field_name]
		        if self.is_valid() else
		        self.fields[field_name].initial)


class GlobalSearchView(CommAdminView):
	template_name = "gsearch/search.html"
	search_title = "Resultados da busca"

	def init_request(self, *args, **kwargs):
		super().init_request(*args, **kwargs)
		self.form = SearchForm(data=self.request_params if self.request_method == 'post' else None)
		models = self.form.fields['models']
		models.initial = [v[0] for v in search.choices]
		models.choices = search.choices

	def get_search_view(self, model_option):
		return self.get_view(ListAdminView, model_option)

	def block_nav_form(self, context, nodes):
		context = get_context_dict(context or {})
		nodes.append(render_to_string("gsearch/blocks/search.nav.form.html",
		                              context=context))

	@cached_property
	def request_params(self):
		return self.request.GET if self.request_method == "get" else self.request.POST

	def search(self, request, **kwargs):
		context = self.get_context()
		views = []
		count = 0
		search_val = self.request_params.get(SEARCH_VAR, '')
		search_models = self.form.get_val("models")
		for model in search:
			opts = self.admin_site.get_registry(model)
			model_option = search.get_option(model, opts)
			search_view = self.get_search_view(model_option)
			search_view.setup(request, **kwargs)
			checked = search_view.app_model_name in search_models
			if self.request_method == "get":
				checked &= search_view.model_filter_active
			active = checked and bool(search_val)
			query_string = search_view.get_query_string({
				SEARCH_VAR: search_val
			})
			views.append({
				'view': search_view,
				'url': search_view.model_admin_url("changelist") + query_string,
				'checked': checked,
				'active': active
			})
			if active:
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

	def get_media(self):
		media = super().get_media()
		media += django_forms.Media(js=(
			'gsearch/js/search.models.js',
		))
		return media

	def get(self, request, **kwargs):
		return self.search(request, **kwargs)

	def post(self, request, **kwargs):
		return self.search(request, **kwargs)
