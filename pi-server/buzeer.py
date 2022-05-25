import RPi.GPIO as GPIO
import time

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH) # HIGH should turn the buzzer off

def peep():
    while True:
        GPIO.output(pin, GPIO.LOW) # peep
        time.sleep(1.0)
        GPIO.output(pin, GPIO.HIGH) # should make the buzzer quiet
        time.sleep(3.0)

def tearDown():
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    print('Peeping!')
    setup()
    try:
        peep()
    except KeyboardInterrupt:
        tearDown()