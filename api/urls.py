from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.CourseListView.as_view()),
    path('course/add/', views.CourseCreateView.as_view()),
    path('course/edit/<str:code>/', views.CourseUpdateView.as_view()),
    path('course/delete/<str:code>/', views.CourseDeleteView.as_view()),
    path('course/<str:code>/', views.CourseView.as_view()),

    # recommendations!
    path('recommend/course/<str:code>/',
         views.CourseRecommendationView.as_view()),

    # reviews
    path('reviews/', views.ReviewListView.as_view()),
    path('review/add/', views.ReviewCreateView.as_view()),
    path('review/update/<int:id>/', views.ReviewUpdateView.as_view()),
    #     path('review/delete/<int:id>/', views.ReviewDeleteView.as_view()),
    #     path('review/<int:id>/', views.ReviewView.as_view()),

    #     path('users/', views.UserListView.as_view()),
    path('user/<str:username>/', views.UserDetailView.as_view()),
    path('user/courses/<str:user__username>/',
         views.UserDetailUpdateView.as_view()),
]
