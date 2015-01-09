from django import template
from django.conf import settings
from pymorphy import get_morph

register = template.Library()
morph = get_morph(settings.PYMORPHY_DICTS['ru']['dir'], 'cdb')

@register.filter
def plural_from_object(source, obj):
    l = len(obj[0])
    if 1 == l:
        return source
    return morph.pluralize_inflected_ru(source.upper(), l).lower()