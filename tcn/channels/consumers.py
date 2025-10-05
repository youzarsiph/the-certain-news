"""Consumers"""

from typing import Any, Dict

from channels.generic.websocket import AsyncJsonWebsocketConsumer


# Create your consumers here.
class LiveFeedConsumer(AsyncJsonWebsocketConsumer):
    """Live breaking news feed"""

    groups = []
    language: str

    async def connect(self) -> None:

        self.language = self.scope["url_route"]["kwargs"]["language_code"]
        self.groups = [f"{self.language}-live"]

        await self.channel_layer.group_add(self.groups[0], self.channel_name)

        return await self.accept()

    async def disconnect(self, close_code) -> None:
        await self.channel_layer.group_discard(self.groups[0], self.channel_name)

    async def receive_json(
        self, content: Dict[str, Any], **kwargs: Dict[str, Any]
    ) -> None:
        """Send received breaking news"""

        await self.channel_layer.group_send(
            self.groups[0],
            {
                "type": "broadcast",
                "article": content["article"],
            },
        )

    async def broadcast(self, event: Dict[str, Any]):
        """Broadcast breaking news"""

        await self.send_json(event["article"])
