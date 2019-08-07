# -*- coding: utf-8 -*-
"""
Created on Fri Aug 02 17:04:51 2019

@author: E202770
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^view/(?P<_id>[-\w]+)$', views.doc_view, name='document_detail'),
]