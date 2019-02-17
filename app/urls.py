"""htc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include, url
from accountingOfPersonalExpenses import views

urlpatterns = [
    path('', views.index),
    re_path(r'^add/?$', views.add, name='Добавление нового расхода'),
    re_path(r'^view/month/?$', views.view_month, name='Просмотр расходов за месяц'),
    re_path(r'^view/all/?$', views.view_all, name='Просмотр расходов за все время'),
    re_path(r'^categories/?$', views.categories, name='Редактирование категорий'),
    re_path(r'^categories/delete/(?P<id_categories>\d+)/?$', views.categories_del, name='Удаление категории'),
]

if settings.DEBUG:
   import debug_toolbar
   urlpatterns += [
       url(r'^__debug__/', include(debug_toolbar.urls)),
   ]
