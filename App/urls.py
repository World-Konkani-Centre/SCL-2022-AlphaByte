from multiprocessing import AuthenticationError
from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path

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
    path('User/Success/',views.successpayment,name='success'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='App/reset/resetPassword.html'), name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='App/reset/passwordResetSent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='App/reset/passwordresetForm.html'), name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='App/reset/resetDone.html'), name='password_reset_complete'),
]