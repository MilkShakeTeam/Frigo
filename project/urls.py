# coding=utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # Toutes les urls en app/ gérées par l'application elle même
    url(r'^app/', include('app.urls', namespace="app")),
)
