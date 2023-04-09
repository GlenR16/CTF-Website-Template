from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.views.generic.base import TemplateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,Http404,FileResponse,JsonResponse
from .forms import UserCreationForm,UserLoginForm,PasswordChangeForm
from .models import User,Team,Challenge,CTF
from django.views.decorators.csrf import requires_csrf_token
import uuid

if CTF.objects.first() == None:
    print("Initialising CTF Object.")
    new_ctf = CTF()
    new_ctf.save()
else:
    print("CTF Object exists.")

class IndexView(TemplateView):
    template_name = "index.html"

class PasswordChangeView(LoginRequiredMixin,TemplateView):
    template_name = "password_change.html"
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return render(request,"password_changed.html")
        else:
            return self.render_to_response({"form":form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PasswordChangeForm(self.request.user)
        return context

class SignupView(TemplateView):
    template_name = "signup.html"
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("/dashboard")
        else:
            return self.render_to_response({"form":form,"CTF":CTF.objects.first()})

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/dashboard")
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserCreationForm()
        context["CTF"] = CTF.objects.first()
        return context

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/login")

class LoginView(TemplateView):
    template_name = "login.html"
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request,email=request.POST.get("username",""),password=request.POST.get("password",""))
            login(request,user)
            return redirect("/dashboard")
        else:
            return self.render_to_response({"form":form})

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/dashboard")
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserLoginForm()
        return context

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        if request.user.team != None and request.user.team.disqualified:
            return render(request,"disqualified.html")
        elif CTF.objects.first().started == True:
            return super().get(request, *args, **kwargs)
        else:
            return render(request,"timer.html")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["team"] = Team.objects.get(tid=self.request.user.team.tid)
        except:
            pass
        context["challenge"] = Challenge.objects.all()
        context["CTF"] = CTF.objects.first()
        return context

class FlagView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        if CTF.objects.first().ended != True and CTF.objects.first().started == True and request.user.team != None and request.user.team.disqualified != True:
            flag = request.POST.get("flag","")
            cid = request.POST.get("cid","")
            challenge = get_object_or_404(Challenge,cid=cid)
            team = get_object_or_404(Team,tid=request.user.team.tid)
            if flag != "" and challenge not in team.solved_challenges.all() and challenge.flag == flag:
                team.score += challenge.points
                team.solved_challenges.add(challenge)
                team.save()
                challenge.solved()
                return JsonResponse({'correct': 1})
            else:
                return JsonResponse({'correct': 0})
        else:
            raise Http404

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["CTF"] = CTF.objects.first()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.user.team == None:
            tid = request.POST.get("tid", "")
            name = request.POST.get("name", "")
            if name != "":
                new_team = Team(tid=uuid.uuid4().hex[:8],name=name)
                new_team.save()
                request.user.team = Team.objects.get(tid=new_team.tid)
                request.user.save()
            elif tid != "":
                try:
                    new_team = Team.objects.get(tid=tid)
                except:
                    return render(request,"profile.html",{'error':True})
                if new_team.members_count() < 5:
                    request.user.team = Team.objects.get(tid=tid)
                    request.user.save()
            return HttpResponseRedirect('profile')

class DownloadView(View):
    def get(self, request, *args, **kwargs):
        if "../" in self.kwargs["filename"] or "'" in self.kwargs["filename"] or '"' in self.kwargs["filename"]:
            raise Http404
        try:
            file = open('ctf\\downloads\\'+self.kwargs["filename"],'rb')
            return FileResponse(file)
        except:
            raise Http404

class StatisticsView(TemplateView):
    template_name = "statistics.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["challenge"] = Challenge.objects.all()
        context["team"] = Team.objects.all().order_by('-score')
        return context
