from accounts.models import UserSettings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView
from chat.models import ChatRoom, Message, UserChatRoom

class ChatHomeView(LoginRequiredMixin, TemplateView):
    template_name = "chat.home.html"
    
    def get(self, request, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        context = self.get_context_data(request)
        
        # Get request data sent by user
        message_body = request.POST.get("message-body", "")
        
        if message_body != "":
            new_message = Message.objects.create(
                UserThatPosted=context["user_settings"],
                ChatRoomForMessage=context["chat_room"],
                MessageDateTime=timezone.now(),
                MessageText=message_body
            )
            context["chat_messages"].insert
            (
                0,
                {
                    "username" : context["user_settings"].DisplayName,
                    "text" : new_message.MessageText,
                    "datetime" : new_message.MessageDateTime.strftime("%b %d %Y %H:%M"),
                    "Liked" : False
                }
            )
        
        return render(request, self.template_name, context)
    
    def get_context_data(self, request, **kwargs):
        context = super(ChatHomeView, self).get_context_data(**kwargs)
        
        # General check to see if the chat "General" event exists, all users go into this chat by default
        # TO DO: Make General Default, when we're ready to do more chat rooms, will re-factor this
        if not ChatRoom.objects.filter(DisplayName="General").exists():
            general_chat = ChatRoom.objects.create(DisplayName="General")
        else:
            general_chat = ChatRoom.objects.get(DisplayName="General")
            
        # Check if user is a part of General Chat, if not, add them
        if not UserChatRoom.objects.filter(UserAccount=request.user,ChatRoomForUser=general_chat).exists():
            UserChatRoom.objects.create(UserAccount=request.user,ChatRoomForUser=general_chat)
        
        # Get all messages in this chat
        chat_messages = Message.objects.filter(ChatRoomForMessage=general_chat).order_by("-MessageDateTime")
        context["chat_messages"] = []
        context["chat_room"] = general_chat
        context["user_settings"] = UserSettings.objects.get(UserAccount=request.user)
        
        for msg in chat_messages:
            context["chat_messages"].append(
                {
                    "username" : msg.UserThatPosted.DisplayName, 
                    "text" : msg.MessageText, 
                    "datetime" : msg.MessageDateTime.strftime("%b %d %Y %H:%M"), 
                    "Liked" : False 
                }
            )
        
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