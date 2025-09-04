import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import CustomUser, Chats, ChatRooms
from channels.db import database_sync_to_async

User = CustomUser()  # Assuming CustomUser is your user model


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.connected = True
            # Getting the user from the front-end
            self.user = self.scope["user"]
            print(self.scope, self.scope["user"])
            if self.user.is_anonymous:
                print("Anonymous user - rejecting connection")
                await self.close()
                return
            print(self.user)
            # print(self.scope["url_route"])
            # Getting the other user from the URL
            self.other_user_id = self.scope["url_route"]["kwargs"]["id"]
            try:
                self.other_user = await sync_to_async(CustomUser.objects.get)(username=self.other_user_id)
                print("In the try block")
            except User.DoesNotExist:
                print("User does not exist")
                await self.close()
                return
            except Exception as e:
                print(e)

            self.room_group_name = await sync_to_async(self.get_room_name)(self.user, self.other_user)
            self.chat_room = await sync_to_async(ChatRooms.objects.get)(name=self.room_group_name)
            self.chats = await sync_to_async(lambda: list(self.chat_room.chats.select_related('by', 'to').all()))()
            for chat in self.chats:
                chat.is_read = True
                await sync_to_async(chat.save)()
            self.past = [{"by": chat.by.username, "message": chat.message} for chat in self.chats]

            print(f"Room name: {self.room_group_name}\nChannel name: {self.channel_name}\n{self.chats}")
            print(f"{self.user} connected to {self.room_group_name}")

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': f'you are now connected to the chat socket with {self.other_user.username}',
                'past': self.past,
                'user': self.other_user.username,
            }))
        except Exception as e:
            print(f"Error in connect: {e}")
            await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        to_username = text_data_json.get('to', None)

        # Get the actual CustomUser instance
        to_user = await sync_to_async(CustomUser.objects.get)(username=to_username)
        chat = Chats(to=to_user, by=self.scope["user"], message=message)
        await sync_to_async(chat.save)()
        chat_room = await sync_to_async(ChatRooms.objects.get)(name=self.room_group_name)
        await sync_to_async(chat_room.chats.add)(chat)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope["user"].username,
                'email': self.scope["user"].email,
                'to': text_data_json.get('to', None),  # Optional recipient
                'chat_room': chat_room
            }
        )

        # self.send(json.dumps({
        #             'type': 'chat',
        #             'message': message
        #         }))

    @database_sync_to_async
    def get_user_by_email(self, email):
        return CustomUser.objects.get(email=email)

    async def chat_message(self, event):
        message = event['message']
        user = await self.get_user_by_email(email=event['email'])
        to = event['to']
        if self.scope["user"].email == event['email']:
            status = "sent"
        else:
            status = "received"

        if status == "received":
            chat_room = event['chat_room']
            chats = await sync_to_async(lambda: list(chat_room.chats.select_related('by', 'to').all()))()
            print(f"Chats read:\n{chats}")
            for chat in chats:
                chat.is_read = True
                await sync_to_async(chat.save)()

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'status': status,
            "user": user.username,
            "to": to,
            "email": user.email,
        }))

    def get_room_name(self, user1, user2):
        print("In the get room name function")
        print(user1.id, user2.id)
        ids = sorted([user1.id, user2.id])
        print(f"Creating room name for users: {user1} and {user2}")
        room_name = f"chat_{ids[0]}_{ids[1]}"
        if not ChatRooms.objects.filter(name=room_name).exists():
            chat_room = ChatRooms(user1=user1, user2=user2, name=room_name)
            chat_room.save()
        return room_name

    async def disconnect(self, code):
        self.connected = False
        print("Disconnected", code)
        self.send(json.dumps({
            'type': 'disconnected',
            'message': 'you are now disconnected from the chat socket'
        }))

    @database_sync_to_async
    def get_chats(self, room_name):
        try:
            return list(ChatRooms.objects.get(name=room_name).chats.all().values())
        except ChatRooms.DoesNotExist:
            return []


class Notifications(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            "notifications",
            self.channel_name
        )
        await self.accept()
        await self.send(json.dumps({
            "type": "connection-established",
            "notification": f"{self.user.username} is connected to the notifications socket."
        }))
        self.user.online = True
        await sync_to_async(self.user.save)()
        # notifications = Chats.object.filter(to=self.user, is_read=False, notification_sent=False)

    async def receive(self, text_data):
        print("In receive of notifications.")
        text_data_json = json.loads(text_data)
        print(text_data_json)
        to_username = text_data_json.get("to", None)
        to = await sync_to_async(CustomUser.objects.get)(username=to_username)
        by_username = text_data_json["by"]
        by = await sync_to_async(CustomUser.objects.get)(username=by_username)
        notifications, unread_count = await self.get_notifications(to, by)
        print(notifications, unread_count)
        await self.channel_layer.group_send(
            'notifications',
            {
            "type": "send_notification",
            "notifications": notifications,
            "unread_count": unread_count
            }
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "notifications": event["notifications"],
            "unread_count": event["unread_count"]
        }))

    @database_sync_to_async
    def get_notifications(self, to, by):
        notifications = Chats.objects.filter(to=to, by=by, is_read=False, notification_sent=False)
        unread = Chats.objects.filter(to=to, by=by, is_read=False, notification_sent=False).count()
        notifications = [{"to": notification.to.username, "by": notification.by.username, "notification": notification.message} for notification in notifications]
        return notifications, unread

    async def disconnect(self, code):
        self.user.online = False
        print(self.user.online)
        sync_to_async(self.user.save)()
