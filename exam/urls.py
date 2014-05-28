from django.conf.urls import url,patterns


urlpatterns = patterns('exam.views',
                        url(r'^$', 'home_page'),
                        url(r'^login/$', 'user_login'),
                        url(r'^exam/([\w._-]+)/$', 'exam_access'),
                        url(r'^user-exams/$', 'user_solve_exams'),
                        url(r'^user-exam/([\w._-]+)/$', 'user_exam_question'),
                        url(r'^user-register/$', 'user_register'),
                        url(r'^edit-profile/$', 'edit_profile'),
                        url(r'^get-time/$', 'get_time'),
                        url(r'^exam-start/([\w._-]+)/$', 'exam_start'),
                       )
