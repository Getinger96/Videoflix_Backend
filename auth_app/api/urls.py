from django.urls import path, include
from .views import RegistrationView, ActivationView,CookieTokenObtainPairView,LogoutView,CookieRefreshView,PasswortResetView,PasswortResetConfirmView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('activate/<uidb64>/<token>/', ActivationView.as_view(), name='activate'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswortResetView.as_view(), name='password_reset'),
    path('password_confirm/<uidb64>/<token>/', PasswortResetConfirmView.as_view(), name='password_confirm'),
    
]