from datetime import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from private_chat.models import Private_Message
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = int(text_data_json['author_id'])
        opponent = int(text_data_json['opponent'])

        # save message in database, then return
        private_message = await self.save_message(message, author, opponent)
        message_create_time = datetime.strftime(private_message.create_time, '%d %B %Y г. %H:%M')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': private_message.author.username,
                'author_id': private_message.author.id,
                'create_time': message_create_time
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        create_time = event['create_time']
        author_id = event['author_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'create_time': create_time,
            'author_id': author_id
        }))


    @database_sync_to_async
    def save_message(self, message, author, opponent):
        author = User.objects.filter(id=author)[0]
        opponent = User.objects.filter(id=opponent)[0]
        privat_message = Private_Message(messages=message, author=author)
        privat_message.save()
        privat_message.interlocutors.add(author)
        privat_message.interlocutors.add(opponent)
        return privat_message
