from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import re

def index(request):
    if request.method == 'POST':
        request.session.flush()
    return render(request,'index.html')

emailre = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        if (email!='' and username!='' and password!='' and re.fullmatch(emailre, email) and not Users.objects.filter(email=email)):
            new_user = Users(email=email,name=username,password=password)
            new_user.save()
            request.session['email'] = new_user.email
            return redirect(home)
        else:
            return render(request,'signup.html',{'error':True})
    else:
        session = session_verification(request)
        if session!='':
            return redirect(home)
        else:
            return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            curr_user = Users.objects.get(email=email)
        except:
            curr_user = ''
        if (curr_user!='' and password==curr_user.password):
            request.session['email'] = curr_user.email
            return redirect(home)
        else:
            return render(request,'login.html',{'error':True})
    else:
        session = session_verification(request)
        if session!='':
            return redirect(home)
        else:
            return render(request,'login.html')

def dashboard(request):
    session = session_verification(request)
    if session!='':
        curr_user = Users.objects.get(email=session)
        return render(request,"dashboard.html",{'user':curr_user})
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
        curr_user = Users.objects.get(email=session)
        return render(request,"profile.html",{'user':curr_user})
    else:
        return redirect(login)
