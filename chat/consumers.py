import json
from datetime import datetime

import openai
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from decouple import config

from .models import ChatMessage

openai_api_key = config("OPENAI_API_KEY", default=None)
if openai_api_key:
    openai.api_key = openai_api_key


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        messages = await self.get_last_messages()
        for message in messages:
            message["timestamp"] = message["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            await self.send(text_data=json.dumps(message))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = text_data_json["user"]

        await self.save_message(user, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @sync_to_async
    def save_message(self, user, message):
        ChatMessage.objects.create(user=user, message=message)

    @sync_to_async
    def get_last_messages(self):
        return list(
            ChatMessage.objects.order_by("timestamp").values(
                "user", "message", "timestamp"
            )[:50]
        )


class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = text_data_json.get("user", "anonymous")

        await self.send(text_data=json.dumps({"user": user, "message": message}))

        bot_reply = await self.get_bot_response(message)

        await self.send(
            text_data=json.dumps(
                {
                    "user": "AI Bot",
                    "message": bot_reply,
                }
            )
        )

    async def get_bot_response(self, prompt):
        if not openai.api_key:
            return "OpenAI API key is not configured."

        try:
            response = await sync_to_async(openai.ChatCompletion.create)(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error contacting OpenAI: {e}"
