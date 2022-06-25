from django.urls import path

from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('report/',views.report,name='report'),
    path('addWaste/',views.addWaste,name='addwaste'),
    path('schedule/',views.schedule,name='schedule'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logOutUser,name='logout'),
    path('register/',views.register,name='register'),
    path('Profile/',views.ProfilePage,name='profile'),
    path('awareness/',views.Awareness,name='awareness'),

]