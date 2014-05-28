from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from exam.forms import ValidatingPasswordChangeForm
from exam import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('exam.urls')),
    url(r'^accounts/login/$','exam.views.user_login'),
    url(r'^accounts/password/$',
        'django.contrib.auth.views.password_change',
        {'password_change_form': ValidatingPasswordChangeForm},
        name='password_change'),

    url(r'^accounts/change-password-done/$',
        'django.contrib.auth.views.password_change_done', name='password_change_done'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#captcha
urlpatterns += patterns('',
                        url(r'^captcha/',include('captcha.urls')),
                        )