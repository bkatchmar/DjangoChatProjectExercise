from accounts.models import UserSettings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils import timezone
from django.urls import reverse
from django.views.generic import TemplateView
from chat.models import ChatRoom, Message, UserChatRoom

class ChatHomeView(LoginRequiredMixin, TemplateView):
    template_name = "chat.home.html"
    
    def get(self, request, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        context = self.get_context_data(request, **kwargs)
        
        # Get request data sent by user
        message_body = request.POST.get("message-body", "")
        
        if message_body != "":
            new_message = Message.objects.create(
                UserThatPosted=context["user_settings"],
                ChatRoomForMessage=context["chat_room"],
                MessageDateTime=timezone.now(),
                MessageText=message_body
            )
            context["chat_messages"].insert(0,{
                "username" : context["user_settings"].DisplayName,
                "text" : new_message.MessageText,
                "datetime" : new_message.MessageDateTime.strftime("%b %d %Y %H:%M"),
                "liked" : False})
        
        return render(request, self.template_name, context)
    
    def get_context_data(self, request, **kwargs):
        context = super(ChatHomeView, self).get_context_data(**kwargs)
        
        # Base General Chat Check
        if not ChatRoom.objects.filter(DisplayName="General").exists():
            ChatRoom.objects.create(DisplayName="General")
        
        # Get the chat information requested from the request
        if "chat_id" in kwargs:
            selected_chat = ChatRoom.objects.filter(id=kwargs.get("chat_id")).first()
            
            if selected_chat is None:
                selected_chat = ChatRoom.objects.get(DisplayName="General")
        else:
            selected_chat = ChatRoom.objects.get(DisplayName="General")
        
        # Check if user is a part of General Chat, if not, add them
        if not UserChatRoom.objects.filter(UserAccount=request.user,ChatRoomForUser=selected_chat).exists():
            UserChatRoom.objects.create(UserAccount=request.user,ChatRoomForUser=selected_chat)
        
        # Get all messages in this chat
        chat_messages = Message.objects.filter(ChatRoomForMessage=selected_chat).order_by("-MessageDateTime")
        context["chat_messages"] = []
        context["chat_room"] = selected_chat
        context["user_settings"] = UserSettings.objects.get(UserAccount=request.user)
        
        for msg in chat_messages:
            context["chat_messages"].append({
                "username" : msg.UserThatPosted.DisplayName, 
                "text" : msg.MessageText,
                "datetime" : msg.MessageDateTime.strftime("%b %d %Y %H:%M"), 
                "liked" : False})
        
        return context

class AllChatRoomsView(LoginRequiredMixin, TemplateView):
    template_name = "chat.all.html"
    
    def get(self, request, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super(AllChatRoomsView, self).get_context_data(**kwargs)
        context["chat_rooms"] = ChatRoom.objects.all()
        return context
    
class MyChatRoomsView(LoginRequiredMixin, TemplateView):
    template_name = "chat.my.html"
    
    def get(self, request, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        error_msg = ""
        
        # Get information from the request
        new_chat_name = request.POST.get("new-chat-name", "")
        
        # Some Base Validation Handle
        if new_chat_name == "":
            error_msg = "Name Cannot Be Empty"
        else:
            new_chat = ChatRoom.objects.filter(DisplayName=new_chat_name).first()
            
            if new_chat is None:
                new_chat = ChatRoom.objects.create(DisplayName=new_chat_name)
            
            UserChatRoom.objects.create(UserAccount=request.user,ChatRoomForUser=new_chat)
        
        context = self.get_context_data(request)
        context["error_msg"] = error_msg
        return render(request, self.template_name, context)
    
    def get_context_data(self, request, **kwargs):
        context = super(MyChatRoomsView, self).get_context_data(**kwargs)
        context["chat_rooms"] = UserChatRoom.objects.filter(UserAccount=request.user)
        return context
    
class MySettingsView(LoginRequiredMixin, TemplateView):
    template_name = "user.settings.html"
    
    def get(self, request, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        error_msg = ""
        user_settings = UserSettings.objects.get(UserAccount=request.user)
        
        # Get information from the request
        new_user_name = request.POST.get("new-user-name", "")
        
        # Some Base Validation Handle
        if new_user_name == "":
            error_msg = "Name Cannot Be Empty"
        else:
            user_settings.DisplayName = new_user_name
            user_settings.save()
            return redirect(reverse("chat:home"))
        
        context = self.get_context_data(request)
        context["error_msg"] = error_msg
        return render(request, self.template_name, context)
    
    def get_context_data(self, request, **kwargs):
        context = super(MySettingsView, self).get_context_data(**kwargs)
        return context