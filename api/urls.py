from django.urls import path
from . import views

urlpatterns = [
    path('', views.getCourses),
    path('add/', views.addCourse)
]
