from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(),
         name='auth_register'),
    path('login/', MyTokenObtainPairView.as_view(),
         name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(),
         name='auth_refresh'),
]
