from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   url(r'^get_all_parents$', 'Cottage_Club.main.views.get_only_parent_cottages', name='get_only_parents_ajax'))