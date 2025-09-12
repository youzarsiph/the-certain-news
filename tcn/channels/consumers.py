"""API views"""

from typing import Any, Dict
from channels.generic.websocket import AsyncJsonWebsocketConsumer


# Create your views here.
class LiveFeedConsumer(AsyncJsonWebsocketConsumer):
    """Live breaking news feed"""

    groups = ["broadcast"]

    async def connect(self) -> None:
        return await self.accept()

    async def receive_json(
        self, content: Dict[str, Any], **kwargs: Dict[str, Any]
    ) -> None:
        """Send received breaking news"""

        await self.channel_layer.group_send(
            "broadcast",
            {
                "type": "live.broadcast",
                "article": content["article"],
            },
        )

    async def live_broadcast(self, event: Dict[str, Any]):
        """Broadcast breaking news"""

        await self.send_json(event["article"])
