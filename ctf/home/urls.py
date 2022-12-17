from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('profile',views.profile,name='profile'),
]