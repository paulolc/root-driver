#!/usr/bin/env python
import crc8
import sys
import time
from  rootrobot import RootRobot

# Connect by address. Use "sudo hcitool lescan" to find address.
rr = RootRobot('F9:A7:A8:71:1E:B8')
rr.setspinledanimation(100,0,0)

rr.startdrawing()

for c in range(36):
    rr.drive(40)
    time.sleep(2)
    rr.rotate(10)
    time.sleep(2)

rr.stopdrawing()


time.sleep(2)
rr.stop()

'''
while True:
    try:
        if rr.waitForNotifications(1.0):
            # handleNotification() was called
            continue
    except KeyboardInterrupt:
        print("Bye")
        # Must manually disconnect or you won't be able to reconnect.~
        rr.disconnect()
        sys.exit()

'''
