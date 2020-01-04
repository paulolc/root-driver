#!/usr/bin/env python
import crc8
import sys
import time
from  rootrobot import RootRobot

# Connect by address. Use "sudo hcitool lescan" to find address.
rr = RootRobot('F9:A7:A8:71:1E:B8')
rr.setspinledanimation(100,0,0)
#rr.say("hello")
#rr.batterylevel()

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
devinfosvc = rr.peripheral.getServiceByUUID( UUIDS["RR_DEVICE_INFO_SVC"] )
uartsvc = rr.peripheral.getServiceByUUID( UUIDS["RR_UART_SVC"] )
mychar = devinfosvc.getCharacteristics(forUUID=UUIDS["RR_MANUFACTURER_CHR"])        
print('MANUFACTURER('+UUIDS["RR_MANUFACTURER_CHR"] + '): ' + str(mychar[0].read()))
for s in devinfosvc.peripheral.getCharacteristics():
    print(s)
    if(s.supportsRead()): 
        print(s.read())
print("tx handle: " +  str(rr.tx.getHandle()))
#tx.write(CMDS["FWD"])

# Request some sensor stream.
#bb.cmd(0x02, 0x11, [0, 80, 0, 1, 0x80, 0, 0, 0,   0])

for i in range(255):
    # Set RGB LED colour.
    bb.cmd(0x02, 0x20, [254, i, 2, 0])
    # Wait for streamed data.
    bb.waitForNotifications(1.0)

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


rr.startdrawing()

#for c in range(4):
rr.drive(2000)
time.sleep(5)
rr.rotate(90)
time.sleep(5)

rr.drive(2000)
time.sleep(5)
rr.rotate(90)
time.sleep(5)

rr.drive(2000)
time.sleep(5)
rr.rotate(90)
time.sleep(5)

rr.drive(2000)
time.sleep(5)
rr.rotate(90)
time.sleep(5)


#time.sleep(1)
#rr.drive(1000)
rr.stopdrawing()


#rr.drive(1)
#print('[{}]'.format(', '.join(hex(x) for x in CMDS["LEFT"])))

#rr.tx.write(bytes(CMDS["LEFT"]))

# Dump all GATT stuff.
# rr.dumpCharacteristics()
'''
