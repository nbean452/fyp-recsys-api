from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.getCourses),
    path('course/<str:code>', views.getCourse),
    path('course/add/', views.addCourse),
    path('ratings/', views.getRatings),
    path('rating/<int:id>', views.getRating),
    path('users/', views.getUsers),
    path('user/<int:id>', views.getUser),
]
