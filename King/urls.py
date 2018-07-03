"""King URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from web.views import *
import xadmin
from rest_api.urls import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^add/', add),
    url(r'^delete/', delete),
    url(r'^main/', index),
    url(r'^question/$', qustion_list, name='web-question-list'),
    url(r'^question/([\w\-.+@]+)/$', question_instance, name="web-question-instance"),
    url(r'^questions/([\w\-.+@]+)/$', question_list_filter, name="web-question-filter"),

    url(r'^qu/create/$', question_create, name="web-question-create"),
    url(r'^bank/$', bank_list, name="web-bank-list"),
    url(r'^bank/([\w\-.+@]+)/$',bank_instance, name="web-bank-instance"),
    url(r'^bank-question/([\w\-.+@]+)/$',bank_question_list, name="web-bank-question-list"),
    url(r'^bank-question-add/([\w\-.+@]+)/$',bank_question_add, name="web-bank-question-add"),
    url(r'^bk/create/$', bank_create, name="web-bank-create"),
    url(r'^test/$', test, name="web-test"),
    url(r'^test-answer/$', test_answer, name="web-test-answer"),
    url(r'^for-app/$', for_app, name="web-for-app"),
    url(r'^question/', question),
    url(r'^api/', include(api_patterns)),
]
