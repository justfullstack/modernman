from cgitb import html
from django.urls import path

from customauth.views import SignupView, activationView, AuthenticationView

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
]
