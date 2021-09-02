from typing import Optional
from time import time
from html import escape

from mautrix.types import TextMessageEventContent, MessageType, Format, RelatesTo, RelationType, EventType

from maubot import Plugin, MessageEvent
from maubot.handlers import command

import os
import json
import sqlite3


class Ask(Plugin):

    @staticmethod
    def plural(num: float, unit: str, decimals: Optional[int] = None) -> str:
        num = round(num, decimals)
        if num == 1:
            return f"{num} {unit}"
        else:
            return f"{num} {unit}s"

    @command.new("ask", help="ask question")
    @command.argument("message", pass_raw=True, required=False)
    async def ask_handler(self, evt: MessageEvent, message: str = "") -> None:

        attendee = str(evt.sender)
        question = "".join([attendee,":",message])
        room_id = str(evt.room_id)
        alias_evt = await self.client.get_state_event(evt.room_id, EventType.ROOM_CANONICAL_ALIAS)
        room_name = alias_evt.canonical_alias

        try:
            EVENT_TYPE = EventType.find("com.example.data", EventType.Class.STATE)
            #await self.client.send_state_event(room_id, EVENT_TYPE, content={str(room_id): "blah" }, state_key="foo")
        except Exception as e:
            print(str(e))

        # Get Data in the form of a dict.
        # Matrix won't store state data with double quotes so we have to convert.
        content = await self.client.get_state_event(room_id, EVENT_TYPE, state_key="foo")
        str_obj = str(content.__str__())
        json_str = str_obj.replace("'","\"")
        json_dict = json.loads(json_str)
        
        if not room_id in json_dict.keys():
            json_dict[room_id] = {room_name:{}}
            await self.client.send_state_event(room_id, EVENT_TYPE, content=json_dict, state_key="foo")    
        else:
            rname = list(json_dict[room_id].keys())[0]
            print("rname: "+ rname)
            room_dict = json_dict[room_id][rname]
            nr_keys = int(len(room_dict.keys()))
            next_key = str(int(nr_keys + 1))
            room_dict[next_key] = question

            try:
                await self.client.send_state_event(room_id, EVENT_TYPE, content=json_dict, state_key="foo")
            except Exception as e:
                print(str(e))
            print(str(room_dict))

            content = TextMessageEventContent(
                msgtype=MessageType.NOTICE, format=Format.HTML,
                formatted_body=f"<a href='https://matrix.to/#/{evt.sender}'>{evt.sender}</a>: Thank you! Question submitted.",
                relates_to=RelatesTo(
                rel_type=RelationType("xyz.maubot.ask"),
                event_id=evt.event_id,
            ))
            await evt.respond(content)


    @command.new("qnum", help="Number of Questions")
    async def qnum_handler(self, evt: MessageEvent, message: str = "") -> None:
        room_id = str(evt.room_id)
        alias_evt = await self.client.get_state_event(evt.room_id, EventType.ROOM_CANONICAL_ALIAS)
        room_name = alias_evt.canonical_alias

        try:
            EVENT_TYPE = EventType.find("com.example.data", EventType.Class.STATE)
            #await self.client.send_state_event(room_id, EVENT_TYPE, content={"": ""}, state_key="foo")
        except Exception as e:
            print(str(e))

        content = await self.client.get_state_event(room_id, EVENT_TYPE, state_key="foo")
        str_obj = str(content.__str__())
        json_str = str_obj.replace("'","\"")
        json_dict = json.loads(json_str)

        if not room_id in json_dict.keys():
            await evt.respond("No data.")
            json_dict[room_id] = {}
        else:
            await evt.respond("Number of questions: " + str(len(json_dict[room_id].keys())))


    @command.new("qlist", help="Number of Questions")
    async def qlist_handler(self, evt: MessageEvent, message: str = "") -> None:
        room_id = str(evt.room_id)
        alias_evt = await self.client.get_state_event(evt.room_id, EventType.ROOM_CANONICAL_ALIAS)
        room_name = alias_evt.canonical_alias

        try:
            EVENT_TYPE = EventType.find("com.example.data", EventType.Class.STATE)
        except Exception as e:
            print(str(e))

        content = await self.client.get_state_event(room_id, EVENT_TYPE, state_key="foo")
        str_obj = str(content.__str__())
        json_str = str_obj.replace("'","\"")
        json_dict = json.loads(json_str)

        for k in json_dict.keys():
            if k:
                room_names = list(json_dict[k].keys())
                for i in room_names:
                    string = "Room: " + k + " : " + i
                    print(string)



    @command.new("reset", help="")
    async def reset_handler(self, evt: MessageEvent, message: str = "") -> None:

        room_id = str(evt.room_id)
        alias_evt = await self.client.get_state_event(evt.room_id, EventType.ROOM_CANONICAL_ALIAS)
        room_name = alias_evt.canonical_alias

        try:
            EVENT_TYPE = EventType.find("com.example.data", EventType.Class.STATE)
            await self.client.send_state_event(room_id, EVENT_TYPE, content={"": ""}, state_key="foo")
        except Exception as e:
            print(str(e))



