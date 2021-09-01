from typing import Optional
from time import time
from html import escape

from mautrix.types import TextMessageEventContent, MessageType, Format, RelatesTo, RelationType

from maubot import Plugin, MessageEvent
from maubot.handlers import command


class Info(Plugin):
    @staticmethod
    def plural(num: float, unit: str, decimals: Optional[int] = None) -> str:
        num = round(num, decimals)
        if num == 1:
            return f"{num} {unit}"
        else:
            return f"{num} {unit}s"

    @command.new("info", help="info")
    @command.argument("message", pass_raw=True, required=False)
    async def info_handler(self, evt: MessageEvent, message: str = "") -> None:
        #print(str(dir(evt)))
        #print(str(evt.sender))
        #print(str(evt.room_id))
        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE, format=Format.HTML,
            formatted_body=f"<a href='https://matrix.to/#/{evt.sender}'>{evt.sender}</a>: https://seagl.org/ ",
            relates_to=RelatesTo(
                rel_type=RelationType("xyz.maubot.pong"),
                event_id=evt.event_id,
            ))
        await evt.respond(content)

    #@command.new("echo", help="Repeat a message")
    #@command.argument("message", pass_raw=True)
    #async def echo_handler(self, evt: MessageEvent, message: str) -> None:
    #    await evt.respond(message)
