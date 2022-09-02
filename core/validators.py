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
    pass

#     def post(self, request):

#         data = json.loads(request.body)

#         password1 = data["password1"]

#         # check length
#         if len(password) < 8:
#             return JsonResponse({'password_error': 'Password must be at lease 8 characters long!'}, status=400)

#         # enforce characters
#         if not re.match("[a-z]", str(password)).groups():
#             return JsonResponse({'password_error': 'Password must contain at least one lower case letter!'}, status=400)

#         if not re.match("[A-Z]", str(password)).groups():
#             return JsonResponse({'password_error': 'Password must contain at least one upper case letter!'}, status=400)

        


        
#         if  len(password) > 7 and not re.findall("\W", str(password)):
#             return JsonResponse({'password_error': 'Weak password! Please include at least one special character.'}, status=400)

        
#         if  len(password) > 7 and len(re.findall("\W", str(password))) < 2:
#             return JsonResponse({'password_medium': 'OK password! You can do better though.'}, status=400) 

#         return JsonResponse({'password_strength': 'Excellent password!'}, status=400) 
    


#         return JsonResponse({'password_valid': True}, status=200)

        
