#!/usr/bin/env python

# Root Robot Bluetooth Low Energy Protocol Documentation:
# https://github.com/RootRobotics/root-robot-ble-protocol

import crc8
import sys
from bluepy import btle
import time


PAYLOADMAXBYTES = 16
MSGMAXBYTES = 19

UUIDS = {
      "RR_SN_CHR"            : "00002a25-0000-1000-8000-00805f9b34fb"
    , "RR_FWVER_CHR"         : "00002a26-0000-1000-8000-00805f9b34fb"
    , "RR_HWVER_CHR"         : "00002a27-0000-1000-8000-00805f9b34fb"
    , "RR_MANUFACTURER_CHR"  : "00002a29-0000-1000-8000-00805f9b34fb"
    , "RR_STATE_CHR"         : "00008bb6-0000-1000-8000-00805f9b34fb"

    , "RR_DEVICE_INFO_SVC"   : "0000180a-0000-1000-8000-00805f9b34fb"
    , "RR_ROOT_ID_SVC"       : "48c5d828-ac2a-442d-97a3-0c9822b04979"

    , "RR_UART_SVC"          : "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
    , "RR_TX_CHR"            : "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    , "RR_RX_CHR"            : "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
}

CMDS = {
    "FWD" : [0x01,0x04,0x00,0x00,0x00,0x00,0x64,0x00,0x00,0x00,0x64,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xD1],
    "BACK": [0x01,0x04,0x00,0xFF,0xFF,0xFF,0x9C,0xFF,0xFF,0xFF,0x9C,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x71],
    "STOP": [0x01,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7E],
    "LEFT": [0x01,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x64,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x8A],
    "RIGHT": [0x01,0x04,0x00,0x00,0x00,0x00,0x64,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x25],
    "LEDANIMATION": [0x01,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7E]
}

def to_4bytes(n):
    return list(bytearray(n.to_bytes(4,byteorder='big')))


class RootCommand():
    COMMANDS = {
        "GET_VERSIONS"                      : { "device":  "0" , "command":  "0" },
        "SET_NAME"                          : { "device":  "0" , "command":  "1" },
        "GET_NAME"                          : { "device":  "0" , "command":  "2" },
        "STOP_AND_RESET"                    : { "device":  "0" , "command":  "3" },
        "DISCONNECT"                        : { "device":  "0" , "command":  "6" },
        "GET_SERIAL_NUMBER"                 : { "device":  "0" , "command": "14" },
        "STOP_PROJECT"                      : { "device":  "0" , "command":  "4" },
        "SET_LEFT_AND_RIGHT_MOTOR_SPEED"    : { "device":  "1" , "command":  "4" },
        "SET_LEFT_MOTOR_SPEED"              : { "device":  "1" , "command":  "6" },
        "SET_RIGHT_MOTOR_SPEED"             : { "device":  "1" , "command":  "7" },
        "DRIVE_DISTANCE"                    : { "device":  "1" , "command":  "8" },
        "ROTATE_ANGLE"                      : { "device":  "1" , "command": "12" },
        "SET_MARKER_ERASER_POSITION"        : { "device":  "2" , "command":  "0" },
        "SET_LED_ANIMATION"                 : { "device":  "3" , "command":  "2" },
        "GET_COLOR_SENSOR_DATA"             : { "device":  "4" , "command":  "1" },
        "PLAY_NOTE"                         : { "device":  "5" , "command":  "0" },
        "STOP_NOTE"                         : { "device":  "5" , "command":  "1" },
        "SAY_PHRASE"                        : { "device":  "5" , "command":  "4" },
        "GET_BATTERY_LEVEL"                 : { "device": "14" , "command":  "1" },
        "ENABLE_EVENTS"                     : { "device":  "0" , "command":  "7" },
        "DISABLE_EVENTS"                    : { "device":  "0" , "command":  "9" },
        "GET_ENABLED_EVENTS"                : { "device":  "0" , "command": "11" },

        "GET_VERSIONS_RESPONSE"             : { "device":  "0" , "command":  "0" },
        "GET_NAME_RESPONSE"                 : { "device":  "0" , "command":  "2" },
        "GET_ENABLED_EVENTS_RESPONSE"       : { "device":  "0" , "command": "11" },
        "GET_SERIAL_NUMBER_RESPONSE"        : { "device":  "0" , "command": "14" },
        "DRIVE_DISTANCE_FINISHED_RESPONSE"  : { "device":  "1" , "command":  "8" },
        "ROTATE_ANGLE_FINISHED_RESPONSE"    : { "device":  "1" , "command": "12" },
        "MARKER_ERASER_POSITION_FINISHED_RESPONSE" : { "device":  "2" , "command":  "0" },
        "COLOR_SENSOR_DATA_RESPONSE"        : { "device":  "4" , "command":  "1" },
        "PLAY_NOTE_FINISHED_RESPONSE"       : { "device":  "5" , "command":  "0" },
        "SAY_PHRASE_FINISHED_RESPONSE"      : { "device":  "5" , "command":  "4" },
        "GET_BATTERY_LEVEL_RESPONSE"        : { "device": "14" , "command":  "1" },
        "GET_ENABLED_EVENTS_RESPONSE"       : { "device":  "0" , "command": "11" },
        
        "MOTOR_STALL_EVENT"                 : { "device":  "1" , "command": "29" },
        "COLOR_SENSOR_EVENT"                : { "device":  "4" , "command":  "2" },
        "BUMPER_EVENT"                      : { "device": "12" , "command":  "0" },
        "LIGHT_EVENT"                       : { "device": "13" , "command":  "0" },
        "BATTERY_LEVEL_EVENT"               : { "device": "14" , "command":  "0" },
        "TOUCH_SENSOR_EVENT"                : { "device": "17" , "command":  "0" },
        "CLIFF_EVENT"                       : { "device": "20" , "command":  "0" }
    }

    def __init__(self, command):
        cmd = RootCommand.COMMANDS[ command ]
        self.name = command
        self.device = int(cmd["device"])
        self.command = int(cmd["command"])


class RootRobot(btle.DefaultDelegate):
    def __init__(self, deviceAddress):
        btle.DefaultDelegate.__init__(self)

        # Address type must be "random" or it won't connect.
        self.peripheral = btle.Peripheral(deviceAddress, btle.ADDR_TYPE_RANDOM)
        self.peripheral.setDelegate(self)

        self.seq = 0
        uartsvc = self.peripheral.getServiceByUUID( UUIDS["RR_UART_SVC"] )
        rxchars = uartsvc.getCharacteristics( forUUID=UUIDS["RR_RX_CHR"])
        print("rxchars: " + str(rxchars))
        self.tx = uartsvc.getCharacteristics( forUUID=UUIDS["RR_TX_CHR"])[0]
        self.rx = rxchars[0]
        print("rx properties: " + self.rx.propertiesToString())
        print("rx characteristic handle(" + str(self.rx.getHandle()+1)+ "): " +  str(self.peripheral.readCharacteristic( self.rx.getHandle() + 1) ))
        self.peripheral.writeCharacteristic( self.rx.getHandle()+1 , bytes([0x01,0x00]) )
        print("rx characteristic handle(" + str(self.rx.getHandle()+1)+ "): " +  str(self.peripheral.readCharacteristic( self.rx.getHandle() + 1) ))

        self.erasing = False
        self.drawing = False

    def nextid(self):
        if( self.seq == 255 ):
            self.seq = 0
        else:
            self.seq = self.seq + 1
        return self.seq
    
    def gencmd(self, command, payload):
        cmd = RootCommand(command)
        seqnr = self.nextid()
        cmdbytes = [ cmd.device, cmd.command, seqnr ]
        cmdbytes.extend( payload + [0]*PAYLOADMAXBYTES )
        cmdbytes = cmdbytes [:MSGMAXBYTES] 
        print("cmdbytes w/o crc: " + str(cmdbytes))
        cmdbytes.extend( self.crc(cmdbytes) )
        print("cmdbytes(" + str(len(cmdbytes))+ "): " + str(cmdbytes))
        print('[{}]'.format(', '.join(hex(x) for x in cmdbytes)))
        return bytes(cmdbytes)

    def crc(self,data):
        crc = crc8.crc8()
        crc.update(bytes(data))
        return crc.digest()

    def send(self, data):
        self.tx.write(data,withResponse=True)

    def setspinledanimation(self,red,green,blue):
        LEDSPINANIMATION = 3
        cmdbytes = self.gencmd( "SET_LED_ANIMATION", [LEDSPINANIMATION, red,green,blue] )
        self.send(cmdbytes)
    
    def moveforward(self,speed):
        cmdbytes = self.gencmd( "SET_LEFT_AND_RIGHT_MOTOR_SPEED", [0,0,0,speed,0,0,0,speed] )
        self.send(cmdbytes)

    def rotateleft(self,speed):
        cmdbytes = self.gencmd( "SET_LEFT_AND_RIGHT_MOTOR_SPEED", [0,0,0,0,0,0,0,speed] )
        self.send(cmdbytes)

    def rotateright(self,speed):
        cmdbytes = self.gencmd( "SET_LEFT_AND_RIGHT_MOTOR_SPEED", [0,0,0,speed,0,0,0,0] )
        self.send(cmdbytes)

    def stop(self,speed):
        cmdbytes = self.gencmd( "SET_LEFT_AND_RIGHT_MOTOR_SPEED", [0,0,0,0,0,0,0,0] )
        self.send(cmdbytes)

    def drive(self,milimeters):
        cmdbytes = self.gencmd( "DRIVE_DISTANCE", to_4bytes(milimeters) )
        self.send(cmdbytes)

    def rotate(self,degrees):
        cmdbytes = self.gencmd( "ROTATE_ANGLE", to_4bytes(degrees*10) )
        self.send(cmdbytes)

    def batterylevel(self):
        self.send(self.gencmd("GET_BATTERY_LEVEL",[]))

    def starterasing(self):
        self.stopdrawing()
        self.erasing = True
        self.send(self.gencmd("SET_MARKER_ERASER_POSITION",[2]))

    def stoperasing(self):
        if self.erasing:
            self.erasing = False
            self.send(self.gencmd("SET_MARKER_ERASER_POSITION",[0]))

    def startdrawing(self):
        self.stoperasing()
        self.drawing = True
        self.send(self.gencmd("SET_MARKER_ERASER_POSITION",[1]))

    def stopdrawing(self):
        if self.drawing:
            self.erasing = False
            self.send(self.gencmd("SET_MARKER_ERASER_POSITION",[0]))




    def say(self, phrase):
        phrasebytes = bytearray()
        phrasebytes.extend( phrase.encode())

        print('[{}]'.format(', '.join(hex(x) for x in phrasebytes)))
        cmdbytes = self.gencmd( "SAY_PHRASE", list(phrasebytes) )
        self.send(cmdbytes)

    def handleNotification(self, cHandle, data):
        print('Notification (', cHandle, "): " )
        print('[{}]'.format(', '.join(hex(x) for x in data)))
        print()

    def waitForNotifications(self, time):
        self.peripheral.waitForNotifications(time)

    def disconnect(self):
        self.peripheral.disconnect()
