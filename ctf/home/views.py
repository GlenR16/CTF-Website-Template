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

def signup(request):
    session = session_verification(request)
    if request.method == 'POST' and session == "":
        email = request.POST.get("email", "")
        name = request.POST.get("name", "")
        password = request.POST.get("password", "")
        if (email!='' and name!='' and password!='' and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) and not User.objects.filter(email=email)):
            new_user = User(email=email,name=name,password=password)
            new_user.save()
            request.session['email'] = new_user.email
            return redirect(dashboard)
        else:
            return render(request,'signup.html',{'error':True})
    else:
        if session!='':
            return redirect(dashboard)
        else:
            return render(request,'signup.html')

def login(request):
    session = session_verification(request)
    if request.method == 'POST' and session == "":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        try:
            user = User.objects.get(email=email)
            if (user!='' and password==user.password):
                request.session['email'] = user.email
                return redirect(dashboard)
        except:
            pass
        return render(request,'login.html',{'error':True})
    else:
        if session!='':
            return redirect(dashboard)
        else:
            return render(request,'login.html')

def dashboard(request):
    session = session_verification(request)
    if session!='':
        user = User.objects.get(email=session)
        if user.team != None and user.team.disqualified == True:
            return render(request,'disqualified.html',{'user':user})
        if CTF.objects.first().wave1 == True:
            challenge = Challenge.objects.all()
            if CTF.objects.first().wave2 == True:
                    return render(request,"dashboard.html",{'user':user,'challenge':challenge})
            else:
                return render(request,"dashboard.html",{'user':user,'challenge':challenge[:15]})
        else:
            return render(request,"timer.html",{'user':user})
    else:
        return redirect(login)
    
def session_verification(request):
    try:
        session = request.session['email']
    except:
        session = ''
    return session

def flag(request):
    session = session_verification(request)
    if request.method=="POST" and session!='':
        flag = request.POST.get("flag","")
        cid = request.POST.get("cid","")
        try:
            user = User.objects.get(email=session)
            challenge = Challenge.objects.get(cid=cid)
            team = Team.objects.get(tid=user.team.tid)
        except:
            return redirect(dashboard)
        if flag != "" and challenge.flag == flag and user.team.disqualified != True:
            team.score += challenge.points
            team.save()
            challenge.solved()
        return redirect(dashboard)

def profile(request):
    session = session_verification(request)
    if session!='':
        user = User.objects.get(email=session)
        if request.method=='POST' and user.team == None:
            tid = request.POST.get("tid", "")
            name = request.POST.get("name", "")
            if name != "":
                new_team = Team(name=name)
                new_team.save()
                tid = new_team.tid
            else:
                try:
                    new_team = Team.objects.get(tid=tid)
                except:
                    return render(request,"profile.html",{'user':user,'error':True})
            if len(User.objects.filter(team=new_team))<5:
                try:
                    user.team = Team.objects.get(tid=tid)
                    user.save()
                except:
                    return render(request,"profile.html",{'user':user,'error':True})
            return render(request,"profile.html",{'user':user})
        else:
            user = User.objects.get(email=session)
            rank = list(Team.objects.all().order_by('score').values_list('tid', flat=True)).index(user.team.tid) + 1
            return render(request,"profile.html",{'user':user,'rank':rank})
    else:
        return redirect(login)
    
