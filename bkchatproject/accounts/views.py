from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from accounts.models import UserSettings

class AccountCreationView(TemplateView):
    template_name = "account.create.html"
    
    def get(self, request):
        logout(request) # Just gonna log the user out by default
        return render(request, self.template_name)
    
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
        
        """
        Even though the HTML5 form validation should prevent this, for Unit test purposes I want to make sure values
        Are entered for username, first_name, and both passwords
        """
        if username == "" or first_name == "" or password_1 == "" or password_2 == "":
            did_the_validation_pass = False
            context["error_msg"] = "Not all required fields are filled in"
            return render(request, self.template_name, context)
        
        # Check to see if this user already exists
        if User.objects.filter(username=username).exists():
            did_the_validation_pass = False
            context["error_msg"] = ("A user by the login id of '%s' already exists" % (username))
            return render(request, self.template_name, context)
        
        # Try to create the user especially concerning if the password is a good password
        created_user = User.objects.create(username=username,email=username,first_name=first_name,last_name=last_name,is_staff=False,is_active=False,is_superuser=False)
        try:
            validate_password(password_1,created_user)
            created_user.is_active = True
            created_user.set_password(password_1)
            created_user.save()
            
            # Create the settings record
            UserSettings.objects.create(UserAccount=created_user,DisplayName=first_name)
        except ValidationError as val:
            context["error_msg"] = val.__str__()
            created_user.delete()
            did_the_validation_pass = False
        
        if did_the_validation_pass:
            login(request, created_user)
            return redirect(reverse("chat:home"))
        else:
            return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super(AccountCreationView, self).get_context_data(**kwargs)        
        return context
    
class AccountLoginView(TemplateView):
    template_name = "account.login.html"
    
    def get(self, request):
        logout(request) # Just gonna log the user out by default
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = self.get_context_data()
        
        username = request.POST.get("username" , "")
        password = request.POST.get("password", "")
        
        login_attempt = authenticate(username=username, password=password)
        
        if login_attempt is None:
            context["error_msg"] = "Login Failed, please check your username and password"
            return render(request, self.template_name, context)
        else:
            login(request, login_attempt)
            return redirect(reverse("chat:home"))
    
    def get_context_data(self, **kwargs):
        context = super(AccountLoginView, self).get_context_data(**kwargs)        
        return context