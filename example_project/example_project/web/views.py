# Create your views here.

from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext


class Test1(View):
    def get(self, request):
        return render_to_response("base.jinja", {},
            context_instance=RequestContext(request))


class Test2(View):
    def get(self, request):
        return render_to_response("base.html", {},
            context_instance=RequestContext(request))
