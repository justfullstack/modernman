
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from customauth.views import SignupView, activationView, AuthenticationView
from core.validators import EmailValidationView, PasswordOneValidationView

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
