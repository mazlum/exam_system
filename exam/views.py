from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from exam.forms import *
from django.contrib.auth import *

def home_page(request):
    return render_to_response('home_page.html', locals(), context_instance=RequestContext(request))


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