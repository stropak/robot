from pyPS4Controller.controller import Controller
import motors

move = motors.Motors()

DEFAULT_SPEED = 50


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        print("dopredu")
        move.change_speed(DEFAULT_SPEED)
        move.forward()

    def on_x_release(self):
        print("stop")
        move.brake()

    def on_left_arrow_press(self):
        move.change_speed(DEFAULT_SPEED)
        print("doleva")
        move.left()

    def on_right_arrow_press(self):
        move.change_speed(DEFAULT_SPEED)
        print("doprava")
        move.right()

    def on_left_right_arrow_release(self):
        print("stop")
        move.brake()

    def on_square_press(self):
        move.change_speed(DEFAULT_SPEED)
        print("dozadu")
        move.backward()

    def on_square_release(self):
        print("stop")
        move.brake()

    def on_R3_up(self, value):
        x = value
        x_normalized = x * -100 / 32767
        print("R3XXX"+str(value))
        print(x_normalized)
        move.change_speed_right(x_normalized)
        move.forward()

    def on_R3_y_at_rest(self):
        print("Y rest")
        move.change_speed_right(0)

    def on_L3_up(self, value):
        x = value
        x_normalized = x * -100 / 32767

        print(x_normalized)
        move.change_speed_left(x_normalized)
        move.forward()

    def on_L3_y_at_rest(self):
        print("Y rest")
        move.change_speed_left(0)

    def on_R3_down(self, value):
        x = value
        x_normalized = x * 100 / 32767
        print(x_normalized)
        move.change_speed_right(x_normalized)
        move.backward()

    def on_R3_y_at_rest(self):
        print("Y rest")
        move.change_speed_right(0)

    def on_L3_down(self, value):
        x = value
        x_normalized = x * 100 / 32767
        print(x_normalized)
        move.change_speed_left(x_normalized)
        move.backward()

    def on_L3_y_at_rest(self):
        print("Y rest")
        move.change_speed_left(0)


move.start()
move.change_speed(0)
controller = MyController(interface="/dev/input/js0",
                          connecting_using_ds4drv=False)
controller.listen()
