from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from exam import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'exam_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

)
