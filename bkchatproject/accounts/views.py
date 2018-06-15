from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.generic import TemplateView

class AccountCreationView(TemplateView):
    template_name = "account.create.html"
    
    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = self.get_context_data()
        context["error_msg"] = ""
        
        # Get data entered by user
        username = request.POST.get("username", "")
        first_name = request.POST.get("first-name", "")
        last_name = request.POST.get("last-name", "")
        password_1 = request.POST.get("password-1", "")
        password_2 = request.POST.get("password-2", "")
        
        # Check valid
        did_the_validation_pass = True
        
        # Passwords must match
        if password_1 != password_2:
            did_the_validation_pass = False
            context["error_msg"] = "Passwords must match"
            return render(request, self.template_name, context)
        
        # Try to create the user especially concerning if the password is a good password
        created_user = User.objects.create(username=username,email=username,first_name=first_name,last_name=last_name,is_staff=False,is_active=False,is_superuser=False)
        try:
            validate_password(password_1,created_user)
            created_user.set_password(password_1)
        except ValidationError as val:
            context["error_msg"] = val.__str__()
            created_user.delete()
            did_the_validation_pass = False
        
        if did_the_validation_pass:
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super(AccountCreationView, self).get_context_data(**kwargs)        
        return context