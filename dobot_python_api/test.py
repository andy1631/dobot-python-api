#!/usr/bin/env python

import api

port = input("Enter port:")

api.connect(port)

while True:
    action = input(">> ")

    match action:
        case 'send':
            api.send_message(138, 0x00, b'\x01\x02\x10')
        case 'read':
            print(api.read_message())
        case 'exit':
            break;


api.disconnect()
