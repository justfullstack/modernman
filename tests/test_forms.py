
from django.forms import ValidationError
from django.test import TestCase
from django.core import mail
from customauth.forms import UserCreationForm


class TestAuthenticationForm(TestCase):
    def test_form_validation_works_correctly(self):

        form = UserCreationForm()

        self.assertIsInstance(form, UserCreationForm)
        self.assertFalse(form.is_bound)

        form = UserCreationForm({
            'first_name': 'First',
                                'last_name': 'Last',
                                'email': 'email@domain.com',
                                'password1': 'abcDE123$',
                                'password2': 'abcDE123$'
                                })

        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

        post_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@domain.com',
            'password1': 'abcDE123$',
            'password2': 'abcDE123$'
        }

        form = UserCreationForm(post_data)

        self.assertTrue(form.is_valid())
        self.assertRaises(ValidationError)

        # ensure required field can't be left blank
        form1 = UserCreationForm({
            'first_name': 'First',
            'last_name': '',
            'email': 'email@domain.com',
            'password1': 'abcDE123$',
            'password2': 'abcDE123$'
        }
        )

        # ensure required field can't be left blank
        form2 = UserCreationForm({
            'first_name': 'First',
            'last_name': 'Last',
            'email': '',
            'password1': 'abcDE123$',
            'password2': 'abcDE123$'
        }
        )

        for form in [form1, form2]:
            self.assertFalse(form.is_valid())
            self.assertRaises(ValidationError)

    def testValidSignupFormSendsEmail(self):
        post_data = {
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@domain.com',
            'password1': 'abcDE123$',
            'password2': 'abcDE123$'
        }

        form = UserCreationForm(post_data)

        self.assertTrue(form.is_valid())

        with self.assertLogs('customauth.forms', level='INFO') as logs:
            form.send_mail()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to Modernman')
        self.assertEqual(len(logs.output), 2)
