"""TestTask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from task_app.views import staff, positions, create_position, del_position, update_position, create_employee, \
    update_employee, del_employee, render_index, render_positions, render_create_employee, render_edit_employee, \
    get_employee, render_edit_position, get_position, render_create_position

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('staff/', staff),
    path('positions/', positions),
    path('create_position/', create_position),
    path('del_position/', del_position),
    path('update_position/', update_position),
    path('create_employee/', create_employee),
    path('update_employee/', update_employee),
    path('del_employee/', del_employee),
    path('get_employee/', get_employee),
    path('get_position/', get_position),
    path('', render_index),
    path('app/positions/', render_positions),
    path('app/create_employee/', render_create_employee),
    path('app/edit_employee/', render_edit_employee),
    path('app/edit_position/', render_edit_position),
    path('app/create_position/', render_create_position),
]
