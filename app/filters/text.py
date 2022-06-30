from typing import Union

from aiogram.dispatcher.filters.filters import Filter
from aiogram.types import CallbackQuery, InlineQuery, Message, Poll


class HasText(Filter):
    def __init__(self, has_text: bool = True):
        self.has_text = has_text

    async def check(self, obj: Union[Message, CallbackQuery,
                                     InlineQuery, Poll]) -> bool:
        if isinstance(obj, Message):
            text = obj.text or obj.caption or ""
            if not text and obj.poll:
                text = obj.poll.question
        elif isinstance(obj, CallbackQuery):
            text = obj.data
        elif isinstance(obj, InlineQuery):
            text = obj.query
        elif isinstance(obj, Poll):
            text = obj.question
        else:
            return False

        if text.isspace():
            return not self.has_text
        if not text:
            return not self.has_text
        return self.has_text
        
