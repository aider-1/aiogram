import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from app.utils.generate import get_ids_array

class AccessMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.allowed_ids = get_ids_array()
    
    async def __call__(
            self,
            handler,
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id in self.allowed_ids:
            return await handler(event, data)
        else:
            return await event.answer("Отказано в доступе ❌")