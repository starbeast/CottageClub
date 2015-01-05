from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.serializers.json import DjangoJSONEncoder
from Cottage_Club.main.models import Cottage

import json

from Cottage_Club.main.models import Cottage


def get_only_parent_cottages(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    objects = Cottage.objects.filter(structure=Cottage.PARENT).values('pk')
    result = json.dumps(list(objects), ensure_ascii=False, cls=DjangoJSONEncoder)
    return HttpResponse(content=result, content_type='application/javascript')


def get_category_for_parent(request):
    value = request.GET.get('id', None)
    if value or not request.is_ajax():
        category = Cottage.objects.get(id=value).category
        result = json.dumps({'name': category.name, 'value': category.id}, ensure_ascii=False, cls=DjangoJSONEncoder)
        return HttpResponse(content=result, content_type='application/json')
    else:
        return HttpResponseBadRequest()


