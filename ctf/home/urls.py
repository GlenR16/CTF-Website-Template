from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('profile',views.profile,name='profile'),
    path('statistics',views.statistics,name='statistics'),
    path('flag',views.flag,name='flag'),
    path('downloads/<str:filename>', views.downloads)
]