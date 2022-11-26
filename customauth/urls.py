
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from customauth.views import SignupView, activationView, AuthenticationView
from core.validators import EmailValidationView, PasswordOneValidationView
from django.contrib.auth.views import LogoutView

urlpatterns = [


    path(
        'signup/',
        SignupView.as_view(),
        name='signup'
    ),


    path(
        'activate/<uidb64>/<token>/',
        activationView,
        name='activate'
    ),

    path(
        'login/',
        AuthenticationView.as_view(),
        name='login'
    ),
    
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),

    path(
        'validate-email/',
        csrf_exempt(EmailValidationView.as_view()),
        name='validate-email'
    ),

    path(
        'validate-password1/',
        csrf_exempt(PasswordOneValidationView.as_view()),
        name='validate-password1'
    ),
]
