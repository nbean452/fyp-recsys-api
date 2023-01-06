from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseListView.as_view()),
    path('course/<str:code>', views.CourseView.as_view()),
    path('course/add/', views.addCourse),
    path('ratings/', views.getRatings),
    path('rating/<int:id>', views.RatingView.as_view()),
    path('users/', views.UserListView.as_view()),
    path('user/<int:id>', views.UserView.as_view()),
]
