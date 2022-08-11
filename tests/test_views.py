from django.test import TestCase
from django.urls import reverse
from customauth.forms import UserCreationForm


class TestPage(TestCase):
    def test_user_signup_page_loads_correctly(self):

        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/signup.html")
        self.assertContains(response, "Join ModernMan")
        self.assertIsInstance(response.context["form"], UserCreationForm)
