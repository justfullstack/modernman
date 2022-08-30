from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.utils import timezone
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from customauth.forms import AuthenticationForm, UserCreationForm
import logging


from customauth.models import CustomUser

logger = logging.getLogger(__name__)


class SignupView(View):

    def get(self, request):

        form = UserCreationForm()

        return render(request, "auth/signup.html", {"form": form})

    def post(self, request):

        form = UserCreationForm(request.POST)

        if form.is_valid():
            # gather data
            first_name = request.POST.get("first_name").title()
            last_name = request.POST.get("last_name").title()
            email = request.POST.get("email")
            password = request.POST.get("password1")
            is_subscribed = request.POST.get("is_subscribed")

            # ensure user does not already exist
            try:
                CustomUser.objects.get(email=email)
                messages.error(request, "Email address already registered!")

            except CustomUser.DoesNotExist:

                user = CustomUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    is_subscribed=is_subscribed
                )

                user.is_active = False
                user.save()

                # send welcome email
                form.send_mail()

                # generate activation data
                token = token_generator.make_token(user)
                uidb64 = urlsafe_b64encode(force_bytes(user.pk))

                domain = get_current_site(request).domain

                link = reverse(
                    'activate',
                    kwargs={'uidb64': uidb64, 'token': token}
                )

                activate_url = f"http://{domain}{link}"

                # send activation  email
                email_subject = "Activate Your Account"
                email_body = f"Hello {user.first_name.title()},\nPlease user the link below to activate account!\n{activate_url}."

                mail = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email='noreply@modernman.com',
                    to=[email, ],
                )

                mail.send(fail_silently=False)

                logger.info(f'Activation email successfully sent to {email}')

                messages.success(request, "You signed up successfully!")

                messages.info(
                    request, "Please check your inbox to activate your account.")

                logger.info(f"Account created successfully for {email}...!")

                return redirect("home")

        return render(request, "auth/signup.html", {"form": form})


def activationView(request, uidb64, token):
    # decode id
    id = force_str(urlsafe_b64decode(uidb64))

    # get user
    user = CustomUser.objects.get(pk=id)

    if user.is_active:
        messages.success(request, "Account already activated!")
        return redirect('login')

    # check link validity
    if not token_generator.check_token(user, token):
        messages.error(request, "Token already used!")

    # activate
    user.is_active = True
    user.save()

    logger.info(f"Account activated successfully for user {user.email}...!")

    messages.success(request, "Account activated successfully!")
    return redirect('login')


class AuthenticationView(View):
    def get(self, request):

        form = AuthenticationForm()
        return render(request, "auth/login.html", {"form": form})

    def post(self, request):

        form = AuthenticationForm(request.POST)

        email = request.POST.get("email")
        raw_password = request.POST.get("password")

        try:
            # ensure user exists
            user = CustomUser.objects.get(email=email)
            # ensure user account is activated
            if not user.is_active:
                messages.error(
                    request, "Your account is inactive. Please check your mailbox for an activation link!")
                return redirect('login')

            if user.check_password(raw_password):
                login(request, user)

                # update user last login
                user.last_login = timezone.now()

                messages.success(
                    request, f"Welcome {user.first_name}, You're now logged in.")
                return redirect('products')
            else:
                messages.error(request, "Wrong password!")

        except CustomUser.DoesNotExist:
            messages.error(request, "A user with that email was not found!")

        # ensure user is active

        # check pasword
        # login
        return render(request, "auth/login.html", {"form": form})
