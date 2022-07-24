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
    path('User/Profile/',views.ProfilePage,name='profile'),
    path('User/Subscriptions/',views.subscriptions,name='subscriptions'),
    path('User/Analytics/',views.Charts,name='charts'),
    path('awareness/',views.Awareness,name='awareness'),
    path('RegisterInfo/',views.updateInfo,name='updateInfo'),

]