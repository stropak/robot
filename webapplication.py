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
    print("serva nefunguji")

net_info = networkinfo.NetworkInfo()

try:
    ultrasonic_sensor = ultrasonic.Ultrasonic()
except:
    ultrasonic_sensor = ultrasonicold.UltrasonicOld()

batery_voltmeter = voltmeter.Voltmeter()

websocket_clients = []

# TCP port pro WebSocket server
TCP_PORT = 8889

# Plánovač každých 600 ms spouští funkci pro získaní hodnoty z dálkoměru
scheduler_ultrasonic = ioloop.PeriodicCallback(
    lambda: asyncio.ensure_future(loop_ultrasonic()), 600)

# Plánovač každých 10s spouští funkci pro zjištění signálu wifi
scheduler_signal = ioloop.PeriodicCallback(
    lambda: asyncio.ensure_future(loop_signal()), 10000)

# Plánovač každých 20s spouští funkci pro zjištění stavu baterie
scheduler_battery = ioloop.PeriodicCallback(
    lambda: asyncio.ensure_future(loop_batery()), 20000)

# Odeslání zprávy všem připojeným WebSocket klientům


def websocket_send(message):
    for websocket_client in websocket_clients:
        websocket_client.write_message(message)

# dalkomer


async def loop_ultrasonic():
    distance = ultrasonic_sensor.get_distance()
    websocket_send("D" + str(distance))

# sila wifi


async def loop_signal():
    signal = net_info.get_wifi_signal()
    websocket_send("W" + str(signal))

# indikator baterie


async def loop_batery():
    voltage = batery_voltmeter.get_battery_percent()
    websocket_send("V" + str(voltage))


# WebSocket server
class WebSocketConnection(websocket.WebSocketHandler):

    # povolí navázání spojení i z vnějších stránek
    def check_origin(self, origin):
        return True

    # Pokud se připojí klient, je uložen do seznamu
    def open(self):
        websocket_clients.append(self)
        print("klient pripojen")
        print(len(websocket_clients))
        self.write_message("Klient připojen")
        self.write_message("W" + str(net_info.get_wifi_signal()))
        # Pokud se jedná o prvního klienta, nastartují se motory a spustí se plánovače
        if len(websocket_clients) == 1:
            move.start()
            scheduler_ultrasonic.start()
            scheduler_battery.start()
            scheduler_signal.start()

    # Pokud se odpojí klient, je odstraněn ze seznamu
    def on_close(self):
        websocket_clients.remove(self)
        print("klient odpojen")
        print(len(websocket_clients))
        # Pokud se odpojili všichni klienti, vypnnou se motory
        if len(websocket_clients) == 0:
            move.stop()
            scheduler_ultrasonic.stop()
            scheduler_signal.stop()
            scheduler_battery.stop()

    # Pokud od klienta dorazila nějaká zpráva
    def on_message(self, message):

        try:
            # Znaky F, B, L, R a X slouží k řízení pásů, znaky CL, CR, CU, CD, CC slouží k otáčení kamery
            if message == "F":
                move.forward()
                self.write_message("Tank: Potvrzuji směr: F")
                print("dopredu")
            elif message == "B":
                move.backward()
                self.write_message("Tank: Potvrzuji směr: B")
                print("dozadu")
            elif message == "L":
                move.left()
                self.write_message("Tank: Potvrzuji směr: L")
                print("doleva")
            elif message == "R":
                move.right()
                self.write_message("Tank: Potvrzuji směr: R")
                print("doprava")
            elif message == "LF":
                move.turn_left()
                print("dopredu a doleva")
            elif message == "RF":
                move.turn_right()
                print("dopredu a doprava")
            elif message == "RB":
                move.turn_right_back()
                print("dozadu a doprava")
            elif message == "LB":
                move.turn_left_back()
                print("dozadu a doleva")
            elif message == "X":
                move.brake()
                self.write_message("Tank: Potvrzuji směr: X")
            elif message == "CL":
                camera.left()
                print("kamera doleva")
            elif message == "CR":
                print("kamera doprava")
                camera.right()
            elif message == "CU":
                print("kamera nahoru")
                camera.up()
            elif message == "CD":
                print("kamera dolu")
                camera.down()
            elif message == "CC":
                print("kamera center")
                camera.center()

            # nastavení rychlosti
            elif message[:1] == "S":
                move.change_speed(int(message[1:]))
                self.write_message(
                    "Robot: Potvrzuji rychlost: " + message[1:] + " %")
            else:
                self.write_message("Robot: Neznámá zpráva")
        except:
            print("Chyba v komunikaci")


# Vytvoření WebSocket spojení
app = web.Application([
    (r'/ws', WebSocketConnection)
])


# Běh programu
if __name__ == "__main__":

    # Pole pro WebSocket klienty

    try:
        # Zjisti moji IP adresu na rozhraní WLAN0
        ip = net_info.get_ip()

        # Uvitaci hláška
        print("**** Zdraví Robot ****")
        print("Rozhraní websocketu: http://{}:{}\r\n".format(ip, TCP_PORT))

        # WebSocket poslouchá na portu 8889
        app.listen(TCP_PORT)

        # Spuštění hlavního programu (asynchronní smyčka)
        asyncio.get_event_loop().run_forever()

    except:
        # V případě chyby
        # zastav plánovače
        scheduler_ultrasonic.stop()
        scheduler_signal.stop()
        scheduler_battery.stop()
        # zastav motory
        move.brake()
        GPIO.cleanup()
        print("Ukončuji program")
