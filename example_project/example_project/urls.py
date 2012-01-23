from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from example_project.web.views import Test1

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example_project.views.home', name='home'),
    # url(r'^example_project/', include('example_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^test1/$', Test1.as_view(), name='test-1'),
)
