# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from exam.forms import *
from django.contrib.auth import *
from exam.models import *
from django.contrib.auth.decorators import login_required


##User can solve return exams from this function
def user_exams(request):
    exams_groups = GroupExam.objects.filter(group__in=request.user.groups.all())
    have_exams = []
    for exams_group in exams_groups.all():
        for exam in exams_group.exam.all():
            have_exams.append(exam)
    return have_exams


#Home page
@login_required
def home_page(request):
    have_exams = user_exams(request)
    ##Solved exams
    answered_exam = UserExam.objects.filter(user=request.user)
    for ae in answered_exam:
        have_exams.remove(ae.exam)
    return render_to_response('exams.html', locals(), context_instance=RequestContext(request))


#User login
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


@login_required
def user_exam_question(request, exam_slug):
    try:
        exam = UserExam.objects.get(exam__name_slug=exam_slug, user=request.user, exam__see=True).exam

        questions = Question.objects.filter(exam=exam)
    except Exam.DoesNotExist:
        danger = "Sorry, you don't have this exam."
    except UserExam.DoesNotExist:
        danger = "Sorry, you don't have this exam."

    return render_to_response('user_exam_question.html', locals(), context_instance=RequestContext(request))

@login_required
def user_solve_exams(request):
    exams = UserExam.objects.filter(user=request.user, exam__see=True)
    return render_to_response('user_exams.html', locals(), context_instance=RequestContext(request))


i=0
@login_required
def exam_access(request, exam_slug):
    global i

    try:
        exam = Exam.objects.get(name_slug=exam_slug)
        if not exam in user_exams(request):
            danger = "You don't have permission for solve this exam."
            return render_to_response('exam_access.html', locals(), context_instance=RequestContext(request))

        if UserExam.objects.filter(user=request.user, exam=exam).count():
            danger = "You answered this question."
            return render_to_response('exam_access.html', locals(), context_instance=RequestContext(request))

        ## Exam not started
        if exam.start == False:
            danger = "This exam not started yet."
            return render_to_response('exam_access.html', locals(), context_instance=RequestContext(request))
        ##Exam questions
        questions = Question.objects.filter(exam=exam)
        if questions.count() <= 0:
            danger = "This exam don't have got questions."
            return render_to_response('exam_access.html', locals(), context_instance=RequestContext(request))

        ##Unanswered question
        unanswered = QuestionUserAnswer.objects.filter(exam=exam, question__in=questions[:(i+1)])
        if unanswered.count() < i:
                warning = "You have got unanswered question."


        #Get question
        question = questions[i]

        #Get question answers
        answers = Answer.objects.filter(question=question)

        ##Did user answered question?
        question_user_answer = QuestionUserAnswer.objects.filter(user=request.user, exam=exam, question=question)
        #Get question count for exam
        exam_question_count = Question.objects.filter(exam=exam).count()

        if request.method == "POST":
            if "back" in request.POST:
                i -= 1
                return HttpResponseRedirect('/exam/'+exam.name_slug)

            if "reply" in request.POST:

                question_answer = request.POST.get('answer')

                if question_answer == None:
                    i += 1
                    return HttpResponseRedirect('/exam/'+exam.name_slug)
                else:
                    if not question_answer.isdigit():
                        return HttpResponseRedirect('/exam/'+exam.name_slug)

                    #if answered this question delete before adding
                    answer_control = QuestionUserAnswer.objects.filter(user=request.user, question=question)
                    if answer_control.count() > 0:
                        answer_control.delete()
                    add_answer = QuestionUserAnswer(user=request.user, exam=exam, question=question, answer=Answer.objects.get(id=question_answer))
                    add_answer.save()

                    ##is question last?
                    if i != exam_question_count-1:
                        i += 1
                        return HttpResponseRedirect('/exam/'+exam.name_slug)

                    try:
                        #Get user true answer
                        true_answer = QuestionUserAnswer.objects.filter(user=request.user, exam=exam, answer__true=True).count()
                        #Add UserExam user exam and point
                        user_exam_add = UserExam(user=request.user, exam=exam, point=true_answer).save()
                        #delete QuestionUserAnswer user exam answers
                        #QuestionUserAnswer.objects.filter(user=request.user, exam=exam).delete()

                        add_success = "Thank you. You successfully finished the exam."
                        i = 0
                    except:
                        danger = "Sorry, We have a problem."

    except Exam.DoesNotExist:
        danger = "Sorry, we don't have this exam."

    return render_to_response('exam_access.html', locals(), context_instance=RequestContext(request, {'i': i}))


##User Sign Up
def user_register(request):
    if request.method == "POST":
        register_form = UserCreateForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            info = "Registration is successful. Administrators are waiting for the approval. "
    else:
        register_form = UserCreateForm()
    return render_to_response('create_user.html', locals(), context_instance=RequestContext(request))


def edit_profile(request):

    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        editprofil_form = EditProfileForm(request.POST, instance=user)
        if editprofil_form.is_valid():
            editprofil_form.save()
            info = "Editing was succesfully."
    else:
        editprofil_form = EditProfileForm(initial=user.__dict__)

    return render_to_response('edit_profil.html',locals(),context_instance=RequestContext(request))