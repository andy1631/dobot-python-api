#!/usr/bin/env python

import dobot
import api

port = input("Enter port:")

seri = dobot.create_connection(port)

while seri != None and seri.is_open:
    action = input(">> ")

    match action:
        case 'send':
            api.send_message(138, 0x00, b'\x01\x02\x10', seri)
        case 'read':
            print(api.receive_message(seri))
        case 'exit':
            break;


api.disconnect(seri)
