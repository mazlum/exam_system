from django.conf.urls import url,patterns


urlpatterns = patterns('exam.views',
                        url(r'^$', 'home_page'),
                        url(r'^login/$', 'user_login'),
                        url(r'^exam/([\w._-]+)/$', 'exam_access'),
                       )