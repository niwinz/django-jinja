# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django_jinja import views

from .views import BasicTestView

urlpatterns = patterns('',
    url(r'^test1/$', BasicTestView.as_view(), name='test-1'),
    url(r'^test1/(?P<data>\d+)/$', BasicTestView.as_view(), name='test-1'),
    url(r'^test/404$', views.PageNotFound.as_view(), name="page-404"),
    url(r'^test/403$', views.PermissionDenied.as_view(), name="page-403"),
    url(r'^test/500$', views.ServerError.as_view(), name="page-500"),
)
