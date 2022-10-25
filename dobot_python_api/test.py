#!/usr/bin/env python

import dobot
import api

port = input("Enter port:")

serial = dobot.create_connection(port)

while serial != None and serial.is_open:
    action = input(">> ")

    match action:
        case 'get_home':
            print(dobot.get_home(serial))
        case 'home':
            dobot.home(serial)
        case 'exit':
            break;


api.disconnect(serial)
