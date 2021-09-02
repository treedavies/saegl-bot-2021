from typing import Optional
from time import time
from html import escape

from mautrix.types import TextMessageEventContent, MessageType, Format, RelatesTo, RelationType

from maubot import Plugin, MessageEvent
from maubot.handlers import command

import os
import sqlite3


CREATE_QUESTION_TABLE = """
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY ASC,
    Timestamp DATE DEFAULT (datetime('now','localtime')),
    userid TEXT,
    channel TEXT,
    url TEXT
);
"""


class Createroom(Plugin):

    @staticmethod
    def plural(num: float, unit: str, decimals: Optional[int] = None) -> str:
        num = round(num, decimals)
        if num == 1:
            return f"{num} {unit}"
        else:
            return f"{num} {unit}s"

    @command.new("createroom", help="Create Video-chat room")
    @command.argument("message", pass_raw=True, required=False)
    async def createroom_handler(self, evt: MessageEvent, message: str = "") -> None:

        cursor = ""
        userid = os.getlogin()
        base_dir = "".join(["/home/",userid,"/.seagl-bot-2021/"])
        ASK_DB_PATH = "".join([base_dir,"jitsi-rooms-db.sqlite"])

        # Create DB file if it does not exist
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        if not os.path.exists(ASK_DB_PATH):
            connection = sqlite3.connect(ASK_DB_PATH)
            try:
                cursor = connection.cursor()
                cursor.execute(CREATE_QUESTION_TABLE)
            except Exception as e:
                print("ERROR: ask_handler(): CREATE_QUESTION_TABLE " + str(e))

        # Validate message and form url
        jitsi_url = "https://meet.seattlematrix.org/" + message

        try:
            connection = sqlite3.connect(ASK_DB_PATH)
            cursor = connection.cursor()
            query = """INSERT INTO rooms (userid, channel, url) VALUES (?, ?, ?)"""
            cursor.execute(query, (evt.sender, evt.room_id, jitsi_url))
            connection.commit()
        except Exception as e:
            print("ERROR: ask_handler(): Insert question " + str(e))

        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE, format=Format.HTML,
            formatted_body=f"<a href='https://matrix.to/#/{evt.sender}'>{evt.sender}</a>: Created Room: " + jitsi_url,
            relates_to=RelatesTo(
                rel_type=RelationType("xyz.maubot.ask"),
                event_id=evt.event_id,
            ))
        await evt.respond(content)


    @command.new("listrooms", help="listrooms")
    async def listrooms_handler(self, evt: MessageEvent, message: str = "") -> None:

        obj = StateEventContent{
            "content": {
                "creator": "@example:example.org",
                "m.federate": true,
                "predecessor": {
                    "event_id": "$something:example.org",
                    "room_id": "!oldroom:example.org"
                },
            "room_version": "1"
        },
        "event_id": "$143273582443PhrSn:example.org",
        "origin_server_ts": 1432735824653,
        "room_id": "!jEsUZKDJdhlrceRyVU:example.org",
        "sender": "@example:example.org",
        "state_key": "",
        "type": "m.room.create",
        "unsigned": {
            "age": 1234
        }
        }




        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE, format=Format.HTML,
            formatted_body=f"<a href='https://matrix.to/#/{evt.sender}'>{evt.sender}</a>: https://patch.seagl.org/chat-rooms  ",
            relates_to=RelatesTo(
                rel_type=RelationType("xyz.maubot.createroom"),
                event_id=evt.event_id,
            ))
        await evt.respond(content)


