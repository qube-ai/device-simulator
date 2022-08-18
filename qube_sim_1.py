#!/usr/bin/env python

import asyncio
import websockets
import json
from thing import Thing


SWITCH = True
POWER = True
ENERGY = True
THING_ID = "QUBE-SIM-2"

async def send_message(message, websocket, loc):
    print("Calling from {}".format(loc))
    print("Sending message: {}".format(message))
    try:
        await websocket.send(json.dumps(message))
    except websockets.exceptions.ConnectionClosed as e:
        print("Connection closed [send_message]")
        return

async def message_handler(message, thing: Thing, websocket):
    if message["messageType"] == "getProperty":
        res = thing.get_properties()
        await send_message(res, websocket, "getProperty")

    elif message["messageType"] == "setProperty":
        propertyId = message["data"]["propertyId"]
        new_value  = message["data"]["value"]
        res = thing.set_property(propertyId, new_value)
        await send_message(res, websocket, "setProperty")
        

    elif message["messageType"] == "getThingDescription":
        res = thing.get_td()
        await send_message(res, websocket, "getThingDescription")

    elif message["messageType"] == "getAllThings":
        res = thing.get_tds()
        await send_message(res, websocket, "getAllThings")
    else: 
        print("Unknown message type received: {}".format(message))

            
        

async def connection_handler(thing: Thing):
    uri = "wss://tunnel.qube.eco/ws"
    async with websockets.connect(uri) as websocket:
        print("Got connected")
        print(websocket)
        init_message = {
            "messageType": "StartWs",
        }
        await websocket.send(json.dumps(init_message))
        while True:
            try:
                response = await websocket.recv()
                response = json.loads(response)
                print("Received response: {}".format(response))
                await message_handler(response, thing, websocket)
            except websockets.exceptions.ConnectionClosedError as e:
                print("Connection closed [Main loop]")
                continue


if __name__ == "__main__":
    thing = Thing(THING_ID, SWITCH, POWER, ENERGY)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connection_handler(thing))