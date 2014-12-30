from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   url(r'^get_all_parents$', 'Cottage_Club.main.views.get_only_parent_cottages', name='get_only_parents_ajax'),
   url(r'^get_category_for_parent$', 'Cottage_Club.main.views.get_category_for_parent', name='get_category_for_parent'))