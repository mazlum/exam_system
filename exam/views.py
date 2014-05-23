# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from exam.forms import *
from django.contrib.auth import *
from exam.models import *


##User can solve from this function return exams
def user_exams(request):
    exams_groups = GroupExam.objects.filter(group__in=request.user.groups.all())
    have_exams = []
    for exams_group in exams_groups.all():
        for exam in exams_group.exam.all():
            have_exams.append(exam)
    return have_exams


def home_page(request):
    have_exams = user_exams(request)
    return render_to_response('exams.html', locals(), context_instance=RequestContext(request))


def user_login(request):
    next = request.GET.get('next')
    title = "Login"
    if request.GET.get('logout'):
        if request.user.is_authenticated():
            logout(request)
        HttpResponseRedirect('/')

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        loginForm = LoginForm(data=request.POST)
        if loginForm.is_valid():
            clean_data = loginForm.cleaned_data
            username = clean_data['username']
            password = clean_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next:
                        return HttpResponseRedirect(next)

                    return HttpResponseRedirect('/')
    else:
        loginForm = LoginForm()
    return render_to_response('login.html', locals(), context_instance=RequestContext(request))


##Exam access
def exam_access(request, exam_slug):
    question_id = request.GET.get('question', '1')
    if not question_id.isdigit():
        return HttpResponseRedirect('/')
    try:
        exam = Exam.objects.get(name_slug=exam_slug)
        if not exam in user_exams(request):
            danger = "You don't have permission for solve this exam."
            return render_to_response('exam_access.html', locals(), context_instance=RequestContext(request))

        question = Question.objects.get(exam=exam, id=question_id)

        answers = Answer.objects.filter(question=question)

    except Exam.DoesNotExist:
        danger = "Sorry, we don't have this exam."
    except Question.DoesNotExist:
        danger = "Sorry, we don't have this question for this exam."
    return render_to_response('exam_access.html', locals(), context_instance=RequestContext(request))