from time import sleep
from machine import Pin, PWM
# import machine
import time

# Define the Pin numbers for L298N IN1 to IN4
IN1 = 10
IN2 = 11
IN3 = 13
IN4 = 14

# Set the PWM frequency to 1500Hz (adjust this value as needed)
pwm_freq = 1500


class Motor_Speed_Main:
    def __init__(self, mot_a_forward=IN1, mot_b_forward=IN2, mot_a_back=IN3, mot_b_back=IN4):
        self.a_forward = Pin(mot_a_forward, Pin.OUT)
        self.b_forward = Pin(mot_b_forward, Pin.OUT)
        self.a_back = Pin(mot_a_back, Pin.OUT)
        self.b_back = Pin(mot_b_back, Pin.OUT)
        # Initialize PWM objects for motor control
        self.EN_A = PWM(Pin(12))
        self.EN_B = PWM(Pin(15))

        self.EN_A.freq(pwm_freq)
        self.EN_B.freq(pwm_freq)

    # Set the speed to 50% (you can change this value as needed) range 1 - 0.6 (.5 doesnt move)
    def move_forward(self, speed=0.7):
        print("Moving Forward")
        self.a_forward.value(0)
        self.b_forward.value(1)
        self.a_back.value(0)
        self.b_back.value(1)
        self.EN_A.duty_u16(int(speed * 65535))
        self.EN_B.duty_u16(int(speed * 65535))

    def move_backward(self, speed=0.7):
        print("Moving Backward")
        self.a_forward.value(1)
        self.b_forward.value(0)
        self.a_back.value(1)
        self.b_back.value(0)
        self.EN_A.duty_u16(int(speed * 65535))
        self.EN_B.duty_u16(int(speed * 65535))

    def move_left(self, speed=0.7):
        print("Moving Left")
        self.a_forward.value(0)
        self.b_forward.value(1)
        self.a_back.value(1)
        self.b_back.value(h0)
        self.EN_A.duty_u16(int(speed * 65535))
        self.EN_B.duty_u16(int(speed * 65535))

    def move_right(self, speed=0.7):
        print("Moving Rigt")
        self.a_forward.value(1)
        self.b_forward.value(0)
        self.a_back.value(0)
        self.b_back.value(1)
        self.EN_A.duty_u16(int(speed * 65535))
        self.EN_B.duty_u16(int(speed * 65535))

    def move_stop(self):
        self.a_forward.value(0)
        self.b_forward.value(0)
        self.a_back.value(0)
        self.b_back.value(0)