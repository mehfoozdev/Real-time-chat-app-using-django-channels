from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ChatRoom, ChatMessage

# Create your views here.


def home(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chatapp/index.html', {'chatrooms': chatrooms})



def chatRoom(request, slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    chat_messages = ChatMessage.objects.filter(room=chatroom)[0:30]

    return render(request, 'chatapp/chatroom.html', {'chatroom': chatroom, 'chat_messages': chat_messages})