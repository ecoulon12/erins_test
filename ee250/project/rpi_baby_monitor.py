import paho.mqtt.client as mqtt
import time
import grovepi
from grove_rgb_lcd import *

baby_mode = 1
self_reg_mode = 2
mode = 0
water_sensor = 2
sound_sensor = 0
tears = 0
cries = 0
happiness_level = "n/a"

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    grovepi.pinMode(water_sensor,"INPUT")
    grovepi.pinMode(sound_sensor,"INPUT")
    #subscribe to topics of interest here
    client.subscribe("monitor/mode")
    #init mode to baby monitor
    mode = 1

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_modeMsg(client, userdata, msg): # turn into on_modeMsg
    if str(msg.payload, "utf-8") == "BABY":
        #set mode to baby monitor
        mode = 1
        print("entering baby mode...")
        time.sleep(1)

    elif str(msg.payload, "utf-8") == "SELFREG":
        #set mode to self regulation
        mode = 2
        print("entering self reg mode...")
        time.sleep(1)

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.message_callback_add("monitor/mode", on_modeMsg)
    client.loop_start()
    

    while True:
        # client.publish("FR/ultrasonicRanger", grovepi.ultrasonicRead(USsense))
        # if grovepi.digitalRead(button):
        #     client.publish("FR/button", "Button pressed!")
        time.sleep(.5)
        tears = grovepi.digitalRead(water_sensor)
        cries = grovepi.analogRead(sound_sensor)
        #sample water sensor and sound sensor every half second
        #determine "happiness level" of baby/student
        print(tears)
        print(cries)

        if (mode == baby_mode):
            #publish a message here
            #client.publish("monitor/baby_status", "baby mode")
            print("baby mode")

        elif (mode == self_reg_mode):
            #publish a message here
            #client.publish("monitor/baby_status", "self reg mode")
            print("self reg")

            