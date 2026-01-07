from django.urls import path, include
from .views import RegistrationView, ActivationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('activate/<uidb64>/<token>/', ActivationView.as_view(), name='activate'),
    
]