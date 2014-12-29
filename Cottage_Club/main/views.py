from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import json

from Cottage_Club.main.models import Cottage


def get_only_parent_cottages(request):
    objects = Cottage.objects.filter(structure=Cottage.PARENT).values('pk')
    result = json.dumps(list(objects), ensure_ascii=False, cls=DjangoJSONEncoder)
    return HttpResponse(content=result, content_type='application/javascript')
