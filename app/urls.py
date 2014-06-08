# coding=utf-8
from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<fridge_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<fridge_id>\d+)/add/$', views.add_product, name='add'),
    url(r'^delete/(?P<fridge_id>\d+)/(?P<product_id>\d+)/$', views.delete_product, name='delete'),
    url(r'^add/$', views.add_fridge, name='add_fridge'),
)