# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse


class BasicTestView(View):
    def get(self, request, data=None):
        return HttpResponse("Hello World")


