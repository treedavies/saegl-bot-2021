from typing import Optional
from time import time
from html import escape

from mautrix.types import TextMessageEventContent, MessageType, Format, RelatesTo, RelationType

from maubot import Plugin, MessageEvent
from maubot.handlers import command

import random

RANDOM_TOAST = {
    "0":"'A cup of tea is a cup of peace.' - Soshitsu Sen XV, Tea Life, Tea Mind",
    "1":"'Many kinds of monkeys have a strong taste for tea, coffee and spirituous liqueurs.' - Charles Darwin",
    "2":"'A cup of tea would restore my normality.' - Douglas Adams",
    "3":"'Rainy days should be spent at home with a cup of tea and a good book.' - Bill Watterson",
    "4":"'Honestly, if you're given the choice between Armageddon or tea, you don't say 'what kind of tea?'' - Neil Gaiman",
    "5":"Tea ... is a religion of the art of life. - Kakuzō Okakura",
    "6":"There are few hours in life more agreeable than the hour dedicated to the ceremony known as afternoon tea. - Henry James"
}

class Tea(Plugin):
    @staticmethod
    def plural(num: float, unit: str, decimals: Optional[int] = None) -> str:
        num = round(num, decimals)
        if num == 1:
            return f"{num} {unit}"
        else:
            return f"{num} {unit}s"

    @command.new("tea", help="Tea")
    @command.argument("message", pass_raw=True, required=False)
    async def tea_handler(self, evt: MessageEvent, message: str = "") -> None:
        #print(str(dir(evt)))
        #print(str(evt.sender))
        #print(str(evt.room_id))
        toastee = "".join("@", message.split(" ")[0], ":seattlematrix.org" 
        toast_msg = RANDOM_TOAST[str(random.randint(0,int(len(RANDOM_TOAST.keys()))))]
        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE, format=Format.HTML,
            #formatted_body=f"<a href='https://matrix.to/#/{evt.sender}'>{evt.sender}</a>: {toast_msg}",
            formatted_body=f"<a href='https://matrix.to/#/{toastee}'>{toastee}</a>: {toast_msg}",
            relates_to=RelatesTo(
                rel_type=RelationType("xyz.maubot.pong"),
                event_id=evt.event_id,
            ))
        await evt.respond(content)

    @command.new("echo", help="Repeat a message")
    @command.argument("message", pass_raw=True)
    async def echo_handler(self, evt: MessageEvent, message: str) -> None:
        await evt.respond(message)
