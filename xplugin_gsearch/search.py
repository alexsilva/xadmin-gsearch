# coding=utf-8

class SearchOpts:
	model = None

	def get_queryset(self):
		raise NotImplementedError('get_queryset')


class Search:
	"""Class records that configure search options"""

	def __init__(self):
		self.registry = {}
		self.cache = {}

	def register(self, model, option_class):
		self.registry.setdefault(model, []).append(option_class)

	def get_option(self, model):
		if model in self.cache:
			return self.cache[model]
		opts = model._meta
		options_classes = self.registry[model]
		options = type("".join([opts.__name__ for opts in options_classes] + [opts.app_lable, opts.model_name]),
		               options_classes, {
			               'model': model
		               })
		self.cache[model] = options
		return options

	def get_result_count(self, *models):
		total = 0
		for model in models:
			if model not in self.registry:
				continue
			option = self.get_option(model)
			total += option.get_queryset()
		return total


search = Search()
