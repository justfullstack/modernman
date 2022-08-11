from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from customauth.forms import UserCreationForm
from customauth.models import CustomUser


class AuthenticationView(TestCase):
    def testUserSignupPageLoadsCorrectly(self):

        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/signup.html")
        self.assertContains(response, "Join ModernMan")
        self.assertIsInstance(response.context["form"], UserCreationForm)

    def testUserSignupPageSubmissionWorks(self):
        post_data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "user1@gmail.com",
            "password1": "my_pAssword!",
            "password2": "my_pAssword!",
        }

        with patch.object(UserCreationForm, "send_mail") as mock_send:
            response = self.client.post(
                reverse("signup"),
                post_data
            )

        # confirm redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(
            email=post_data["email"]).exists())
        mock_send.assert_called_once()
