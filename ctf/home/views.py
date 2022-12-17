from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import re
from .models import User,Team,Challenge,CTF
from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
def index(request):
    if request.method == 'POST':
        request.session.flush()
    return render(request,'index.html')

emailre = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def signup(request):
    if request.method == 'POST':
        email = request.POST.get("email", "")
        name = request.POST.get("name", "")
        password = request.POST.get("password", "")
        if (email!='' and name!='' and password!='' and re.fullmatch(emailre, email) and not User.objects.filter(email=email)):
            new_user = User(email=email,name=name,password=password)
            new_user.save()
            request.session['email'] = new_user.email
            return redirect(dashboard)
        else:
            return render(request,'signup.html',{'error':True})
    else:
        session = session_verification(request)
        if session!='':
            return redirect(dashboard)
        else:
            return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        try:
            user = User.objects.get(email=email)
        except:
            user = ''
        if (user!='' and password==user.password):
            request.session['email'] = user.email
            return redirect(dashboard)
        else:
            return render(request,'login.html',{'error':True})
    else:
        session = session_verification(request)
        if session!='':
            return redirect(dashboard)
        else:
            return render(request,'login.html')

def dashboard(request):
    session = session_verification(request)
    if session!='':
        user = User.objects.get(email=session)
        if user.team != '':
            challenge = Challenge.objects.all()
            return render(request,"dashboard.html",{'user':user,'challenge':challenge})
        else:
            return render(request,"dashboard.html",{'user':user})
    else:
        return redirect(login)
    
def session_verification(request):
    try:
        session = request.session['email']
    except:
        session = ''
    return session

def profile(request):
    session = session_verification(request)
    if session!='':
        user = User.objects.get(email=session)
        return render(request,"profile.html",{'user':user})
    else:
        return redirect(login)
    
