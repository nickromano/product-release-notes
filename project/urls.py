from __future__ import absolute_import, unicode_literals

from django.urls import re_path, include
from django.contrib import admin

from django.views.generic import TemplateView


urlpatterns = [
    re_path(r'^', include('product_release_notes.urls')),
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^deploy-instructions/$', TemplateView.as_view(
        template_name="deploy-instructions.html"
    )),
]
