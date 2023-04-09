from django.urls import path
from .views import IndexView,SignupView,LoginView,DashboardView,ProfileView,DownloadView,StatisticsView,FlagView,LogoutView,PasswordChangeView
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('dashboard',DashboardView.as_view(),name='dashboard'),
    path('signup',SignupView.as_view(),name='signup'),
    path('login',LoginView.as_view(),name='login'),
    path('password_change/',PasswordChangeView.as_view(),name='password_change'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile',ProfileView.as_view(),name='profile'),
    path('statistics',StatisticsView.as_view(),name='statistics'),
    path('flag',FlagView.as_view(),name='flag'),
    path('downloads/<str:filename>', DownloadView.as_view(),name="downloads")
]