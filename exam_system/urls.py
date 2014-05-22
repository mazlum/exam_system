from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from exam import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'',include('exam.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
