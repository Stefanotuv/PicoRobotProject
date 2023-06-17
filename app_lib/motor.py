from time import sleep
from machine import Pin


class Motor_Main:
    def __init__(self, mot_a_forward=18,mot_b_forward=19,mot_a_back=20,mot_b_back=21):
        self.a_forward = Pin(mot_a_forward, Pin.OUT)
        self.b_forward = Pin(mot_b_forward, Pin.OUT)
        self.a_back = Pin(mot_a_back, Pin.OUT)
        self.b_back = Pin(mot_b_back, Pin.OUT)

    def move_stop(self):
        self.a_forward.value(0)
        self.b_forward.value(0)
        self.a_back.value(0)
        self.b_back.value(0)

    def move_right(self,time):
        self.a_forward.value(0)
        self.b_forward.value(1)
        self.a_back.value(0)
        self.b_back.value(0)
        if time != "":
            sleep(time)
            self.move_stop()
        sleep(1)
        self.move_stop()

    def move_left(self,time):
        self.a_forward.value(0)
        self.b_forward.value(0)
        self.a_back.value(0)
        self.b_back.value(1)
        if time != "":
            sleep(time)
            self.move_stop()
        sleep(1)
        self.move_stop()

    def move_backward(self,time):
        self.a_forward.value(1)
        self.b_forward.value(0)
        self.a_back.value(0)
        self.b_back.value(1)
        if time != "":
            sleep(time)
            self.move_stop()
        sleep(2)
        self.move_stop()

    def move_forward(self,time):
        self.a_forward.value(0)
        self.b_forward.value(1)
        self.a_back.value(1)
        self.b_back.value(0)
        if time != "":
            sleep(time)
            self.move_stop()
        sleep(2)
        self.move_stop()        