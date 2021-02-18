from django.conf.urls import include, url
from django_jinja import views

from .views import BasicTestView
from .views import I18nTestView, I18nTestViewDTL
from .views import StreamingTestView
from .views import PipelineTestView
from .views import CreateTestView, DeleteTestView, DetailTestView, UpdateTestView
from .views import ListTestView
from .views import ArchiveIndexTestView, YearArchiveTestView, MonthArchiveTestView, WeekArchiveTestView, DayArchiveTestView, TodayArchiveTestView, DateDetailTestView

urlpatterns = [
    url(r"^test1/$", BasicTestView.as_view(), name="test-1"),
    url(r"^test1/(?P<data>\d+)/$", BasicTestView.as_view(), name="test-1"),
    url(r"^test-i18n/$", I18nTestView.as_view(), name="i18n-test"),
    url(r"^test-i18n-dtl/$", I18nTestViewDTL.as_view(), name="i18n-dtl-test"),
    url(r"^test-pipeline/$", PipelineTestView.as_view(), name="pipeline-test"),
    url(r"^test/404$", views.PageNotFound.as_view(), name="page-404"),
    url(r"^test/403$", views.PermissionDenied.as_view(), name="page-403"),
    url(r"^test/500$", views.ServerError.as_view(), name="page-500"),
    url(r"^test-streaming/$", StreamingTestView.as_view(), name='streaming-test'),

    url(r"^testmodel/$", ListTestView.as_view()),
    url(r"^testmodel/create$", CreateTestView.as_view()),
    url(r"^testmodel/(?P<pk>\d+)/delete$", DeleteTestView.as_view()),
    url(r"^testmodel/(?P<pk>\d+)/detail$", DetailTestView.as_view()),
    url(r"^testmodel/(?P<pk>\d+)/update$", UpdateTestView.as_view()),

    url(r"^testmodel/archive/$", ArchiveIndexTestView.as_view()),
    url(r"^testmodel/archive/(?P<year>\d{4})/$", YearArchiveTestView.as_view()),
    url(r"^testmodel/archive/(?P<year>\d{4})/week/(?P<week>\d+)/$", WeekArchiveTestView.as_view()),
    url(r"^testmodel/archive/(?P<year>\d{4})/(?P<month>[\w-]+)/$", MonthArchiveTestView.as_view()),
    url(r"^testmodel/archive/(?P<year>\d{4})/(?P<month>[\w-]+)/(?P<day>\d+)/$", DayArchiveTestView.as_view()),
    url(r"^testmodel/archive/today/$", TodayArchiveTestView.as_view()),
    url(r"^testmodel/archive/(?P<year>\d{4})/(?P<month>[\w-]+)/(?P<day>\d+)/(?P<pk>\d+)$", DateDetailTestView.as_view())
]
