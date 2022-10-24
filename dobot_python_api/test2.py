#!/usr/bin/env python

import api

port = input("Enter port: ")

serial = api.connect(port)

if serial != None and serial.is_open:
    while input() != 'q':
        print(api.receive_message(serial))
    api.disconnect(serial)
