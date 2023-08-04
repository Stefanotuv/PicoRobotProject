from time import sleep
from machine import Pin, PWM

MID = 1375000
MIN = 300000
MAX = 2450000
STEP = 150000


# MID = 5000
# MIN = 1000
# MAX = 9000

class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin, Pin.OUT))
        self.pwm.freq(50)
        self.current_pos = MID
        self.pwm.duty_ns(MID)
        # self.pwm.duty_u16(MID)
        self.name = str(pin)

    #    def initialise(self):
    #        self.pwm.duty_ns(MID)
    #        self.current_pos = MID

    #    def position(self, value):
    #         self.pwm.duty_ns(value)

    def right(self, input=20):
        print("RIGHT")
        print(f'name pin: {self.name}')
        value = int(self.current_pos - int(MID / input))
        print(f'value before: {value}')
        if value > MAX:
            value = MAX
        self.current_pos = value
        self.pwm.duty_ns(value)
        # self.pwm.duty_u16(value)
        print(f'value after: {value}')

    def left(self, input=20):
        print("LEFT")
        print(f'name pin: {self.name}')
        value = int(self.current_pos + int(MID / input))
        print(f'value before: {value}')
        if value < MIN:
            value = MIN
        self.current_pos = value
        self.pwm.duty_ns(value)
        # self.pwm.duty_u16(value)
        print(f'value after: {value}')

    def down(self, input=20):
        print("DOWN")
        print(f'name pin: {self.name}')
        value = int(self.current_pos + int(MID / input))
        print(f'value before: {value}')
        if value > MAX:
            value = MAX
        self.current_pos = value
        self.pwm.duty_ns(value)
        # self.pwm.duty_u16(value)
        print(f'value after: {value}')

    def up(self, input=20):
        print("UP")
        print(f'name pin: {self.name}')
        value = int(self.current_pos - int(MID / input))
        print(f'value before: {value}')
        if value < MIN:
            value = MIN
        self.current_pos = value
        self.pwm.duty_ns(value)
        # self.pwm.duty_u16(value)
        print(f'value after: {value}')

    def center(self):
        print("CENTER")
        print(f'name pin: {self.name}')
        # create a cycle to manage a step by step center
        # value = int(self.current_pos - MID)
        print(f'value before: {self.current_pos}')
        if self.current_pos > MID:
            print("inside if")
            while ((self.current_pos - int(STEP)) > MID):
                print("inside while")
                self.current_pos = self.current_pos - int(STEP)
                self.pwm.duty_ns(self.current_pos)
                sleep(.3)
            self.current_pos = MID
            self.pwm.duty_ns(self.current_pos)
        elif self.current_pos < MID:
            print("inside else")
            while ((self.current_pos + int(STEP)) < MID):
                print("inside while")
                self.current_pos = self.current_pos + int(STEP)
                self.pwm.duty_ns(self.current_pos)
                sleep(.3)
            self.current_pos = MID
            self.pwm.duty_ns(self.current_pos)

        # self.pwm.duty_u16(value)
        print(f'value after: {self.current_pos}')

# test_servo_pan = Servo(2)
# test_servo_tilt = Servo(3)

# test_servo_pan.position(MAX)
# test_servo_tilt.position(MAX)