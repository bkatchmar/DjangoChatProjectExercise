from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

class ChatHomeView(LoginRequiredMixin, TemplateView):
    template_name = "chat.home.html"
    
    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super(ChatHomeView, self).get_context_data(**kwargs)        
        return context