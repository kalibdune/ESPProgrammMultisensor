from umqtt.robust import MQTTClient
import time
import machine
import network
import dht
import json

SSID = "IoT_Case"
PASSWORD = "qweqweqwe"

sensor = dht.DHT11(machine.Pin(5))
rele = machine.Pin(19, machine.Pin.OUT)

def connect_Wifi():
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        print("Already connected")

    station.active(True)
    station.connect(SSID, PASSWORD)

    while station.isconnected() == False:
        pass

def call_back(topic, msg):
    if topic.decode() == 'Dmitry/rele':
        data = json.loads(msg)
        rele.value(int(data["rele"]))
        print("rele turned: ", data["rele"])
        


def setup_MQTT():
    mqtt_server = 'levandrovskiy.ru'
    client_id = "kalibdune"
    client = MQTTClient(client_id=client_id, server=mqtt_server)
    client.connect()
    client.set_callback(call_back)
    client.subscribe("Dmitry/rele")
    return client



connect_Wifi()
client = setup_MQTT()

while True:
    print("cycle")
    client.check_msg()
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    data = {
        "temp": temp,
        "hum": hum
    }
    data = json.dumps(data)
    #print(data)
    client.publish("Dmitry/data", data)
    #rele.value(1)
    time.sleep(2)
    #rele.value(0)
