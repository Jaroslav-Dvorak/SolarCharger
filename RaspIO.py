import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)


def out_on(pin):
    if GPIO.input(pin) == GPIO.LOW:
        GPIO.output(pin, True)


def out_off(pin):
    if GPIO.input(pin) == GPIO.HIGH:
        GPIO.output(pin, False)


def pin_state(pin):
    return GPIO.input(pin) == GPIO.HIGH
