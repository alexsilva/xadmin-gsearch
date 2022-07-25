# coding=utf-8
from xadmin.sites import site
from xadmin.views.base import CommAdminView
from xplugin_gsearch.plugin import GlobalSearchPlugin
from xplugin_gsearch.views.search import GlobalSearchView, GlobalSearchResultView

site.register_view(r"^gsearch/$", GlobalSearchView, "gsearch")
site.register_view(r'^gsearch/r/(?P<app_label>.+)/(?P<model_name>.+)/$',
                   GlobalSearchResultView,
                   name='search_resultlist')

site.register_plugin(GlobalSearchPlugin, CommAdminView)
