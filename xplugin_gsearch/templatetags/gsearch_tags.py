from django import template
from django.apps import apps as django_apps

register = template.Library()


@register.filter
def filters_num(search_views):
	"""filters and counts the total number of views marked as a filter."""
	return len([view for view in search_views if view['checked']])


@register.simple_tag
def filters_all_checked(search_views):
	all_checked = True
	for view in search_views:
		if not view['checked']:
			all_checked = False
			break
	return all_checked
