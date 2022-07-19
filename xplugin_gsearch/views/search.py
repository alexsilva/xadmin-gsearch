# coding=utf-8
import django.forms as django_forms
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.functional import cached_property
from xadmin.filters import SEARCH_VAR
from xadmin.plugins.utils import get_context_dict
from xadmin.views import CommAdminView, ListAdminView
from xplugin_gsearch.search import search


class SearchForm(django_forms.Form):
	shr = django_forms.BooleanField(required=False, initial=False)
	mdl = django_forms.MultipleChoiceField(required=False)

	def clean_mdl(self):
		models = self.cleaned_data['mdl']
		return [int(m) for m in models if m.isdigit()]

	def get_val(self, field_name):
		return (self.cleaned_data[field_name]
		        if self.is_valid() and self.cleaned_data['shr'] else
		        self.fields[field_name].initial)


class GlobalSearchView(CommAdminView):
	template_name = "gsearch/search.html"
	search_title = _("Search results")

	def init_request(self, *args, **kwargs):
		super().init_request(*args, **kwargs)
		self.search_text = self.request_params.get(SEARCH_VAR, '').strip()
		self.form = SearchForm(data=self.request_params)
		models = self.form.fields['mdl']
		models.initial = [v[0] for v in search.choices]
		models.choices = search.choices

	def get_search_view(self, model_option, **opts):
		return self.get_view(ListAdminView, model_option, opts=opts)

	def block_nav_form(self, context, nodes):
		context = get_context_dict(context or {})
		nodes.append(render_to_string("gsearch/blocks/search.nav.form.html",
		                              context=context))

	def get_breadcrumb(self):
		bc = super().get_breadcrumb()
		bc.append({
			'url': None,
			'title': self.search_title
		})
		return bc

	@cached_property
	def request_params(self):
		return self.request.GET if self.request_method == "get" else self.request.POST

	def search(self, request, **kwargs):
		context = self.get_context()
		views = []
		count = 0
		search_model_ids = self.form.get_val("mdl")
		searching = self.form.get_val("shr")
		models_ids = dict([(v, k) for k, v in search.choices])
		for model in search:
			opts = self.admin_site.get_registry(model)
			model_option = search.get_option(model, opts)
			model_filter_id = models_ids[search.get_app_model_name(model)]
			search_view = self.get_search_view(model_option, model_filter_id=model_filter_id)
			search_view.setup(request, **kwargs)
			checked = search_view.model_filter_id in search_model_ids
			if self.request_method == "get" and not searching:
				checked &= search_view.model_filter_active
			active = search_view.has_view_permission() and checked and bool(self.search_text)
			query_string = search_view.get_query_string({
				SEARCH_VAR: self.search_text
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
			'search_text': self.search_text,
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
