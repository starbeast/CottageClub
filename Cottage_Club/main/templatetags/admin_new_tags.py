import json
 
from django import template
from django.core.urlresolvers import reverse
from django.utils.html import mark_safe
from Cottage_Club.main.ajax_urls import urlpatterns

register = template.Library()


@register.simple_tag
def ajax_urls():
    urls = {}
    for x in urlpatterns:
        if getattr(x, 'name', None):
            urls[x.name] = (reverse(x.name))
    return json.dumps(urls)