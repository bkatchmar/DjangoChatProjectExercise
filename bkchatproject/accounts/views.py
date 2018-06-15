from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView

class AccountCreationView(TemplateView):
    template_name = "account.create.html"
    
    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super(AccountCreationView, self).get_context_data(**kwargs)        
        return context