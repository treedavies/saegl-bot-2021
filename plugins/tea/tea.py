from typing import Optional
from time import time
from html import escape

from mautrix.types import TextMessageEventContent, MessageType, Format, RelatesTo, RelationType, EventType
from maubot import Plugin, MessageEvent
from maubot.handlers import command

import random

RANDOM_TOAST = {
    "0":"'A cup of tea is a cup of peace.' - Soshitsu Sen XV, Tea Life, Tea Mind",
    "1":"'Many kinds of monkeys have a strong taste for tea, coffee and spirituous liqueurs.' - Charles Darwin",
    "2":"'A cup of tea would restore my normality.' - Douglas Adams",
    "3":"'Rainy days should be spent at home with a cup of tea and a good book.' - Bill Watterson",
    "4":"'Honestly, if you're given the choice between Armageddon or tea, you don't say 'what kind of tea?'' - Neil Gaiman",
    "5":"'Tea ... is a religion of the art of life.' - Kakuzō Okakura",
    "6":"'There are few hours in life more agreeable than the hour dedicated to the ceremony known as afternoon tea.' - Henry James",
    "7":"'Computer, Earl Gray, Hot.' - Captain Jean Luc Picard",
    "8":"'Good Tea... Nice house.' - Worf - https://tinyurl.com/55jwfcwa",
    "9":"'When tea becomes ritual, it takes place at the heart of our ability to see greatness in small things.' - Muriel Barbery",
    "10":"'If at first, you don’t succeed, have a cup of tea.' - Peter Scott",
    "11":"'Good tea is eloquent enough, it turns out, to change a person’s mind.' - Banana Yoshimoto",
    "12":"'Tea is the magic key to the vault where my brain is kept.' - Frances Hardinge",
    "13":"'I got nasty habits; I take tea at three.' -  Mick Jagger",
    "14":"'Coffee. Now that is my cup of tea.' - Tree Davies",
    "15":"'Tea began as a medicine and grew into a beverage.' - Okakura Kakuzo",
    "16":"'All true tea lovers not only like their tea strong but like it a little stronger with each year that passes.' - George Orwell",
    "17":"'I like Tea...' https://tinyurl.com/24f764bh"
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

        toastee: str
        msg = message.replace(" ","")
        if len(msg) == 0:
            toastee = str(evt.sender)
        else:
            toastee = msg

        toast_msg = RANDOM_TOAST[str(random.randint(0,int(len(RANDOM_TOAST.keys()))))]

        if len(msg) == 0:
            ftxt = f"<a href='https://matrix.to/#/{toastee}'>{toastee}</a>: {toast_msg}"
        else:
            ftxt = f"<a href='https://matrix.to/#/{toastee}'>{toastee}</a>: {evt.sender} is toasting you! {toast_msg}"

        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE, format=Format.HTML,
            formatted_body=ftxt,
            relates_to=RelatesTo(
                rel_type=RelationType("xyz.maubot.tea"),
                event_id=evt.event_id,
            ))
        await evt.respond(content)

    @command.new("echo", help="Repeat a message")
    @command.argument("message", pass_raw=True)
    async def echo_handler(self, evt: MessageEvent, message: str) -> None:
        print(str(dir(evt)))
        print(str(evt.sender))
        print(str(evt.room_id))
        print(str(evt.source))
        print(str(evt.json))
        alias_evt = await self.client.get_state_event(evt.room_id, EventType.ROOM_CANONICAL_ALIAS)
        print("-->"+str(alias_evt.canonical_alias))

        await evt.respond(message)
