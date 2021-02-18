from django.views.generic import View
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader
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

class I18nTestView(View):
    template_name = "i18n_test.jinja"

    def get(self, request, data=None):
        class Author:
            name = "Freddy Fred"

        class Book:
            title = "Big 'ol Book"

        return render(request, self.template_name, {
            "v_index": "Index",
            "table_sort": lambda x, y: "{} {}".format(x, y),
            "invoice_count": 1,
            "trimmed_invoice_count": 2,
            "author": Author(),
            "book": Book(),
        })

class I18nTestViewDTL(I18nTestView):
    template_name = "i18n_test.html"

class PipelineTestView(View):
    def get(self, request, data=None):
        return render(request, "pipeline_test.jinja")

class ContextManipulationTestView(View):
    def get(self, request):
        return render(request, "hello_world.jinja", {"name": "Jinja2"})

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

class StreamingTestView(View):
    def get(self, request, *args, **kwargs):
        context = {"name": "Streaming Jinja2", "view": type(self)}
        template = loader.get_template('streaming_test.jinja')
        return StreamingHttpResponse(template.stream(context, request), content_type='text/html')
