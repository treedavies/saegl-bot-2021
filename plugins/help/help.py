from typing import Optional
from time import time
from html import escape

from mautrix.types import TextMessageEventContent, MessageType, Format, RelatesTo, RelationType

from maubot import Plugin, MessageEvent
from maubot.handlers import command


class Help(Plugin):
    @staticmethod
    def plural(num: float, unit: str, decimals: Optional[int] = None) -> str:
        num = round(num, decimals)
        if num == 1:
            return f"{num} {unit}"
        else:
            return f"{num} {unit}s"

    @command.new("help", help="help")
    @command.argument("message", pass_raw=True, required=False)
    async def help_handler(self, evt: MessageEvent, message: str = "") -> None:
        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE, format=Format.HTML,
            formatted_body=f"<a href='https://matrix.to/#/{evt.sender}'>{evt.sender}</a>: Learn how to interact with SeaGL-bot here:  https://seagl.org/seag-bot/",
            relates_to=RelatesTo(
                rel_type=RelationType("xyz.maubot.help"),
                event_id=evt.event_id,
            ))
        await evt.respond(content)

