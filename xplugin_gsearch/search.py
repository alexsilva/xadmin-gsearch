# coding=utf-8

class SearchOptsView:
	model = opts = None

	def get_label(self):
		return self.opts.verbose_name

	def get_total(self):
		return self.get_list_queryset().count()


class Search:
	"""Class records that configure search options"""

	def __init__(self):
		self.registry = {}
		self.cache = {}
		self._iterator = None

	def register(self, model, option_class):
		try:
			model_options = self.registry[model]
		except KeyError:
			self.registry[model] = model_options = []
		model_options.append(option_class)

	def __iter__(self):
		return iter(self.registry)

	def get_option(self, model, option_base):
		if model in self.cache:
			return self.cache[model]
		opts = model._meta
		bases = [option_base, SearchOptsView] + self.registry[model]
		options = type("".join([opts.__name__ for opts in bases] + [opts.app_label, opts.model_name]),
		               tuple(bases), {
			               'model': model
		               })
		self.cache[model] = options
		return options


search = Search()
