from django import template
from django.apps import apps as django_apps

register = template.Library()


@register.filter
def filters_num(search_views):
	"""filters and counts the total number of views marked as a filter."""
	return len([view for view in search_views if view['checked']])
