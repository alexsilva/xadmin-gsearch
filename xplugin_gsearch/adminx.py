# coding=utf-8
from xadmin.sites import site
from xplugin_gsearch.views.search import GlobalSearchView

site.register_view("gsearch/", GlobalSearchView, "gsearch")
