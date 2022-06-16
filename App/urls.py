from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('report/',views.report),
    path('addWaste/',views.addWaste),
    path('schedule/',views.schedule),

]