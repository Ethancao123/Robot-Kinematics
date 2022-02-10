import RPi.GPIO as GPIO


def switch_callback():
    print("Switch Pressed")


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.FALLING, callback=switch_callback)