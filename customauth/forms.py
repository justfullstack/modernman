import logging
from django.core import validators
from django.core.mail import send_mail
from django import forms


logger = logging.getLogger(__name__)


class UserCreationForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    first_name = forms.CharField(
        label='First Name',
        max_length=20,
        required=True
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length=20,
        required=True
    )

    email = forms.EmailField(
        label='Enter a valid email',
        max_length=20,
        required=True,
        validators=[validators.validate_email, ],
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(render_value=False),
        min_length=8,
        max_length=60,
        required=True
    )

    password2 = forms.CharField(
        label='Repeat Password',
        strip=False,
        widget=forms.PasswordInput(render_value=False),
        min_length=8,
        max_length=60,
        required=True
    )

    is_subscribed = forms.BooleanField(
        label="I want to receive offers in my email",
        initial=False,
        widget=forms.CheckboxInput(),
        required=False
    )

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Both passwords must match!")
        else:
            raise forms.ValidationError("Both passwords are required!")

        return self.cleaned_data

    def send_mail(self):
        logger.info(f"Sending signup email for {self.cleaned_data['email']}")

        from_email = 'welcome@modernman.com'
        to_email = self.cleaned_data.get("email")
        subject = 'Welcome to Modernman'
        message = f"Hi {self.cleaned_data.get('first_name').title()},\nThank you for joining Modernman, the store of choice for every stylish modern man.Experience the best quality and cost in the market. Please check your inbox for an activation email."

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[to_email, ],
            fail_silently=False,
            html_message=None
        )

        logger.info(
            f"Signup email successfully sent to {self.cleaned_data['email']}")

    for field in [first_name, last_name, email, password1, password2, ]:
        field.widget.attrs.update({'class': 'form-control'})

    for field in [first_name, last_name, email, password1, password2, ]:
        field.widget.attrs.update({'placeholder': field.label})

    for field in [is_subscribed]:
        field.widget.attrs.update({'class': 'text-right'})
