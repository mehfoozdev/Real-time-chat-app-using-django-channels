from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage


'''
This class is a subclass of AsyncWebsocketConsumer, 
which is a class that handles WebSocket connections.
''' 
class ChatConsumer(AsyncWebsocketConsumer):

    # Establish connection with WebSocket
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept connection
        await self.accept()
    

    # Disconnect from WebSocket
    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.channel_layer,
            self.room_group_name
        )


    

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room
            }
        )

        # Save message to database
        await self.save_message(message, username, room)

    
    # Send mesage
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room
        }))

    
    
    '''
    The @sync_to_async decorator is used in Python programming, particularly in the context of Django, to convert a synchronous function into an asynchronous one. This allows the function to be run in an asynchronous manner, which is useful when integrating synchronous code into an asynchronous application framework.
    '''
    @sync_to_async
    def save_message(self, message, username, room):
        user = User.objects.get(username=username)
        room = ChatRoom.objects.get(slug=room)
        message = ChatMessage.objects.create(user=user, room=room, message=message)
        message.save()


