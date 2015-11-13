# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from django_jinja.views.generic.detail import DetailView
from django_jinja.views.generic.edit import CreateView, DeleteView, UpdateView
from django_jinja.views.generic.list import ListView
from django_jinja.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView, DateDetailView

from .models import TestModel


class BasicTestView(View):
    def get(self, request, data=None):
        data = render_to_string("hello_world.jinja", {"name": "Jinja2"},
                                request=request)
        return HttpResponse(data)


class PipelineTestView(View):
    def get(self, request, data=None):
        return render_to_response("pipeline_test.jinja", request=request)

class ContextManipulationTestView(View):
    def get(self, request):
        return render(request, "hello_world.jinja", {"name": "Jinja2"}, request=request)

# ==== generic.detail ====
class DetailTestView(DetailView):
    model = TestModel

# ==== generic.edit ====
class CreateTestView(CreateView):
    model = TestModel
    fields = []
    template_name_suffix = '_create'

class DeleteTestView(DeleteView):
    model = TestModel

class UpdateTestView(UpdateView):
    model = TestModel
    fields = []
    template_name_suffix = '_update'

# ==== generic.list ====
class ListTestView(ListView):
    model = TestModel

# ==== generic.dates ====
class ArchiveIndexTestView(ArchiveIndexView):
    model = TestModel
    date_field = 'date'

class YearArchiveTestView(YearArchiveView):
    model = TestModel
    date_field = 'date'

class MonthArchiveTestView(MonthArchiveView):
    model = TestModel
    date_field = 'date'

class WeekArchiveTestView(WeekArchiveView):
    model = TestModel
    date_field = 'date'

class DayArchiveTestView(DayArchiveView):
    model = TestModel
    date_field = 'date'

class TodayArchiveTestView(TodayArchiveView):
    model = TestModel
    date_field = 'date'
    template_name_suffix = '_archive_today'

class DateDetailTestView(DateDetailView):
    model = TestModel
    date_field = 'date'
    template_name_suffix = '_date_detail'
