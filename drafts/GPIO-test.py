import RPi.GPIO as GPIO

pin = 37
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)


# wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
channel = GPIO.wait_for_edge(pin, GPIO.RISING, timeout=10000)
if channel is None:
    print('Timeout occurred')
else:
    print('Edge detected on channel', channel)

GPIO.cleanup()