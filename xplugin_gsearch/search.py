# coding=utf-8


class SearchOptsView:
	model = opts = None
	model_filter_active = True

	@property
	def verbose_name(self):
		return self.opts.verbose_name

	@property
	def app_model_name(self):
		return f"{self.opts.app_label}.{self.opts.model_name}"

	def get_total(self):
		return self.get_list_queryset().count()


class Search:
	"""Class records that configure search options"""

	def __init__(self):
		self.registry = {}
		self.cache = {}
		self._iterator = None

	@property
	def choices(self):
		chs = []
		for model in self.registry:
			opts = model._meta
			name = f"{opts.app_label}.{opts.model_name}"
			chs.append((name, model))
		return chs

	def register(self, model, option_class=None):
		try:
			model_options = self.registry[model]
		except KeyError:
			self.registry[model] = model_options = []
		if option_class is not None:
			model_options.append(option_class)

	def __iter__(self):
		return iter(self.registry)

	def get_option(self, model, option_base):
		if model in self.cache:
			return self.cache[model]
		opts = model._meta
		bases = list(self.registry[model])
		bases.extend([SearchOptsView, option_base])
		options = type("".join([opts.__name__ for opts in bases] + [opts.app_label, opts.model_name]),
		               tuple(bases), {
			               'model': model
		               })
		self.cache[model] = options
		return options


search = Search()
