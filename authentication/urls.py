from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(),
         name='auth_register'),
    path('login/', LoginView.as_view(),
         name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(),
         name='auth_refresh'),
]
