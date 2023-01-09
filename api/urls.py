from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseListView.as_view()),
    path('course/add/', views.CourseCreateView.as_view()),
    path('course/edit/<str:code>', views.CourseUpdateView.as_view()),
    path('course/delete/<str:code>', views.CourseDeleteView.as_view()),
    path('course/<str:code>/', views.CourseView.as_view()),

    path('ratings/', views.RatingListView.as_view()),
    path('rating/add/', views.RatingCreateView.as_view()),
    path('rating/edit/<int:id>', views.RatingUpdateView.as_view()),
    path('rating/delete/<int:id>', views.RatingDeleteView.as_view()),
    path('rating/<int:id>', views.RatingView.as_view()),

    path('users/', views.UserListView.as_view()),
    path('user/<str:username>', views.UserView.as_view()),
]
