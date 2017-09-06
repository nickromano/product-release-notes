from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic import TemplateView


urlpatterns = [
    url(r'^', include('product_release_notes.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^deploy-instructions/$', TemplateView.as_view(
        template_name="deploy-instructions.html"
    )),
]
