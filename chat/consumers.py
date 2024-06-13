import json
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from cryptography.fernet import Fernet

key = b'1xucvqDtuKscCT-iymt4piuTsVQ3tnoI-vdufsUQ2P0='
GUN_SERVER_URL = 'http://localhost:8765/gun'  # Gun server URL

class PersonChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    def encrypt_message(self, message):
        cipher_suite = Fernet(key)
        encrypted_message = cipher_suite.encrypt(message.encode())
        return encrypted_message

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        encrypted_message = self.encrypt_message(message)
        await self.save_message(username, encrypted_message.decode('utf-8'), self.room_group_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def save_message(self, username, encrypted_message, thread_name):
        data = {
            'username': username,
            'message': encrypted_message,
        }
        response = requests.put(f'{GUN_SERVER_URL}/{thread_name}', json=data)
        if response.status_code != 200:
            print(f'Failed to save message: {response.text}')

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )







# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from cryptography.fernet import Fernet

# from .models import UserChatdetails
# from userapp.models import UserDetails
# key = b'1xucvqDtuKscCT-iymt4piuTsVQ3tnoI-vdufsUQ2P0='


# class PersonChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):

#         # user_email = request.session.get('user_email')
#         my_id = self.scope['user'].id
#         print('my_id',my_id)
#         other_user_id = self.scope['url_route']['kwargs']['id']
#         print('other_id', other_user_id)
#         if int(my_id) > int(other_user_id):
#             self.room_name = f'{my_id}-{other_user_id}'
#         else:
#             self.room_name = f'{other_user_id}-{my_id}'
#         self.room_group_name = 'chat_%s' % self.room_name

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#         # await self.send(text_data = self.room_group_name)

    
#     def encrypt_message(sef,message):
#         cipher_suite = Fernet(key)
#         encrypted_message = cipher_suite.encrypt(message.encode())
#         return encrypted_message
    
#     async def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)
#         message = data['message']
#         username = data['username']
#         encrypted_message = self.encrypt_message(message)
#         await self.save_message(username, encrypted_message, self.room_group_name)
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'username': username,
#             }
#         ) 
        
#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']
#         await self.send(text_data= json.dumps({
#             'message' : message ,
#             'username' : username
#         }))

#     @database_sync_to_async
#     def save_message(self, username , encrypted_message,thread_name):
#         UserChatdetails.objects.create(username = username, message = encrypted_message, thread_name = thread_name)



#     async def disconnect(self, code):
#         print('DISCONNECT')
#         self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_layer
#         )
