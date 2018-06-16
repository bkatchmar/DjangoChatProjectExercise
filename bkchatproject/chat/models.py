from accounts.models import UserSettings
from django.contrib.auth.models import User
from django.db import models

class ChatRoom(models.Model):
    DisplayName = models.CharField(max_length=50,null=False)
    
    class Meta:
       db_table = "ChatRoom"
       
class UserChatRoom(models.Model):
    UserAccount = models.ForeignKey(User,on_delete=models.CASCADE)
    ChatRoomForUser = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    
    class Meta:
       db_table = "UserChatRoom"
       
class Message(models.Model):
    UserThatPosted = models.ForeignKey(UserSettings,null=False,on_delete=models.CASCADE)
    ChatRoomForMessage = models.ForeignKey(ChatRoom,null=False,on_delete=models.CASCADE)
    MessageDateTime = models.DateTimeField(auto_now=False,auto_now_add=False,null=False)
    MessageText = models.TextField(null=False)
    
    class Meta:
       db_table = "Message"

class MessageLike(models.Model):
    MessageLiked = models.ForeignKey(Message,null=False,on_delete=models.CASCADE)
    UserWhoLiked = models.ForeignKey(UserSettings,null=False,on_delete=models.CASCADE)
    
    class Meta:
       db_table = "MessageLike"