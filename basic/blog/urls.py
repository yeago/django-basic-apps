from django.conf.urls.defaults import patterns, url
from django.views.generic import dates
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from basic.blog.models import Category, Post


urlpatterns = patterns('basic.blog.views',
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view='post_detail',
        name='blog_detail'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        dates.DayArchiveView.as_view(allow_future=False),
        name='blog_archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        dates.MonthArchiveView.as_view(allow_future=False),
        name='blog_archive_month'
    ),
    url(r'^(?P<year>\d{4})/$',
        dates.YearArchiveView.as_view(allow_future=False),
        name='blog_archive_year'
    ),
    url(r'^categories/(?P<slug>[-\w]+)/$',
        DetailView.as_view(model=Category),
        name='blog_category_detail'
    ),
    url (r'^categories/$',
        ListView.as_view(model=Category),
        name='blog_category_list'
    ),
    url (r'^search/$',
        view='search',
        name='blog_search'
    ),
    #url(r'^page/(?P<page>\d+)/$',
    #    name='blog_index_paginated'
    #),
    url(r'^$',
        ListView.as_view(model=Post),
        name='blog_index'
    ),
)
