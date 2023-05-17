from tornado import websocket, web, ioloop
import asyncio
from time import sleep
import RPi.GPIO as GPIO
from time import time
import os
import re
import motors
import servos
import networkinfo
import ultrasonic
import ultrasonicold
import voltmeter

move = motors.Motors()

try:
    camera = servos.Servos()
except:
    print("servos are not working")

net_info = networkinfo.NetworkInfo()

try:
    ultrasonic_sensor = ultrasonic.Ultrasonic()
except:
    ultrasonic_sensor = ultrasonicold.UltrasonicOld()

batery_voltmeter = voltmeter.Voltmeter()

websocket_clients = []

# TCP port for WebSocket server
TCP_PORT = 8889

# The scheduler every 600 ms runs a function to get the value from the ultrasonic sensor
scheduler_ultrasonic = ioloop.PeriodicCallback(
    lambda: asyncio.ensure_future(loop_ultrasonic()), 600)

# The scheduler every 10s runs a function to detect the wifi signal
scheduler_signal = ioloop.PeriodicCallback(
    lambda: asyncio.ensure_future(loop_signal()), 10000)

# The scheduler every 20s runs a function to check the battery status
scheduler_battery = ioloop.PeriodicCallback(
    lambda: asyncio.ensure_future(loop_batery()), 20000)


# Send the message to all connected WebSocket clients
def websocket_send(message):
    for websocket_client in websocket_clients:
        websocket_client.write_message(message)

# ultrasonic sensor
async def loop_ultrasonic():
    distance = ultrasonic_sensor.get_distance()
    websocket_send("D" + str(distance))

# wifi
async def loop_signal():
    signal = net_info.get_wifi_signal()
    websocket_send("W" + str(signal))

# battery
async def loop_batery():
    voltage = batery_voltmeter.get_battery_percent()
    websocket_send("V" + str(voltage))


# WebSocket server
class WebSocketConnection(websocket.WebSocketHandler):

    # allow connection from external sites 
    def check_origin(self, origin):
        return True

    # If the client connects, save it to the list
    def open(self):
        websocket_clients.append(self)
        print("klient pripojen")
        print(len(websocket_clients))
        self.write_message("Klient připojen")
        self.write_message("W" + str(net_info.get_wifi_signal()))
        # If this is a first time client, activate the motors and start the schedulers
        if len(websocket_clients) == 1:
            move.start()
            scheduler_ultrasonic.start()
            scheduler_battery.start()
            scheduler_signal.start()

    # If the client disconnects, remove it from the list
    def on_close(self):
        websocket_clients.remove(self)
        print("client disconected")
        print(len(websocket_clients))
        # If all clients have disconnected, turn off the motors
        if len(websocket_clients) == 0:
            move.stop()
            scheduler_ultrasonic.stop()
            scheduler_signal.stop()
            scheduler_battery.stop()

    # Pokud od klienta dorazila nějaká zpráva
    def on_message(self, message):

        try:
            # Characters F, B, L, R, RF, RB, LF, LB a X are for movement, characters CL, CR, CU, CD, CC are for camera movement
            if message == "F":
                move.forward()
             elif message == "B":
                move.backward()
            elif message == "L":
                move.left()
            elif message == "R":
                move.right()
            elif message == "LF":
                move.turn_left()
            elif message == "RF":
                move.turn_right()
            elif message == "RB":
                move.turn_right_back()
            elif message == "LB":
                move.turn_left_back()
            elif message == "X":
                move.brake()
            elif message == "CL":
                camera.left()
            elif message == "CR":
                camera.right()
            elif message == "CU":
                camera.up()
            elif message == "CD":
                camera.down()
            elif message == "CC":
                camera.center()

            # set speed
            elif message[:1] == "S":
                move.change_speed(int(message[1:]))
                self.write_message(
                    "Robot: new speed: " + message[1:] + " %")
            else:
                self.write_message("Robot: Unknown message")
        except:
            print("Communication error")


# create WebSocket connection
app = web.Application([
    (r'/ws', WebSocketConnection)
])


# main program 
if __name__ == "__main__":

    try:
        # get IP adress for WLAN0
        ip = net_info.get_ip()

        # Welcome message
        print("**** Zdraví Robot ****")
        print("Rozhraní websocketu: http://{}:{}\r\n".format(ip, TCP_PORT))

        # WebSocket listen on port 8889
        app.listen(TCP_PORT)

        # Run main loop (asynchronous)
        asyncio.get_event_loop().run_forever()

    except:
        # in case of error
        #stop schedulers
        scheduler_ultrasonic.stop()
        scheduler_signal.stop()
        scheduler_battery.stop()
        # stop motors
        move.brake()
        GPIO.cleanup()
        print("Exit")
