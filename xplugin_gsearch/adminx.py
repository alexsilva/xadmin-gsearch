# coding=utf-8
from xadmin.sites import site
from xadmin.views.base import CommAdminView
from xplugin_gsearch.plugin import GlobalSearchPlugin
from xplugin_gsearch.views.search import GlobalSearchView

site.register_view("gsearch/", GlobalSearchView, "gsearch")
site.register_plugin(GlobalSearchPlugin, CommAdminView)
