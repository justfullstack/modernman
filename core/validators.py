import re
from django.views import View
from django.http import JsonResponse
from customauth.models import CustomUser
import json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# AJAX VALIDATION VIEWS
class EmailValidationView(View):

    def post(self, request):

        data = json.loads(request.body)

        email = data["email"]

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'email_valid': False}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'email_valid': False}, status=409)

        return JsonResponse({'email_valid': True}, status=200)


# # AJAX VALIDATION VIEWS
class PasswordOneValidationView(View):

    def post(self, request):

        # get data
        data = json.loads(request.body)
        password1 = data["password1"]

        # weak pass : status 400
        # check length
        if len(password1) < 8:
            return JsonResponse({'password1_valid': False, 'message': 'Password must be at lease 8 characters long!'}, status=400)

        # enforce characters
        if re.search(r"[a-z]", str(password1)) is None:
            return JsonResponse({'password1_valid': False, 'message': 'Password must contain at least one lower case letter!'}, status=400)

        if re.search(r"[A-Z]", str(password1)) is None:
            return JsonResponse({'password1_valid': False, 'message': 'Password must contain at least one UPPER case letter!'}, status=400)

        if re.search(r"\W", str(password1)) is None:
            return JsonResponse({'password1_valid': False, 'message': 'Weak password! Please include at least one special character.'}, status=401)

        if len(password1) > 7 and len(re.findall("\W", str(password1))) < 2:
            return JsonResponse({'password1_valid': False, 'message': 'OK password! You can do better though.'}, status=409)

        return JsonResponse({'password1_valid': True, 'message': 'Excellent password!'}, status=200)
