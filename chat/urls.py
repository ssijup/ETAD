from django.urls import path

from .import views


urlpatterns = [


    path("personalchat", views.personalchat, name="personalchat"),
   


]