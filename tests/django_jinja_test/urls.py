# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from .views import BasicTestView

urlpatterns = patterns('',
    url(r'^test1/$', BasicTestView.as_view(), name='test-1'),
    url(r'^test1/(?P<data>\d+)/$', BasicTestView.as_view(), name='test-1'),
)
