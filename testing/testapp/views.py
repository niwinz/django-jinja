# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render_to_response


class BasicTestView(View):
    def get(self, request, data=None):
        return render_to_response("hello_world.jinja", {"name": "Jinja2"})

class PipelineTestView(View):
    def get(self, request, data=None):
        return render_to_response("pipeline_test.jinja")
