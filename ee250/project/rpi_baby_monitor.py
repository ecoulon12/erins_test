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
buzzer = 8


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    grovepi.pinMode(water_sensor,"INPUT")
    grovepi.pinMode(sound_sensor,"INPUT")
    grovepi.pinMode(buzzer,"OUTPUT")
    #subscribe to topics of interest here
    client.subscribe("monitor/response")
    #init mode to baby monitor
    mode = 1

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_modeMsg(client, userdata, msg): # turn into on_modeMsg
    if str(msg.payload, "utf-8") == "BABY":
        #set mode to baby monitor
        mode = 1
        #print("entering baby mode...")
        time.sleep(1)

    elif str(msg.payload, "utf-8") == "SELFREG":
        #set mode to self regulation
        mode = 2
        #print("entering self reg mode...")
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
        tears = not grovepi.digitalRead(water_sensor)
        cries = grovepi.analogRead(sound_sensor)
        #sample water sensor and sound sensor every half second
        #determine "happiness level" of baby/student
        print("tears: ", tears, "sound: ", cries)
        if(cries<150 and not tears):
            client.publish("monitor/status", "happy!")
        elif (cries<150 and tears):
            client.publish("monitor/status", "crying level 1")
            grovepi.digitalWrite(buzzer,1)
            time.sleep(.5)
            grovepi.digitalWrite(buzzer,0)            
        elif(cries<300 and tears):
            client.publish("monitor/status", "crying level 2")
        elif(cries<500 and tears):
            client.publish("monitor/status", "crying level 3")
        elif(cries>500 and tears):
            client.publish("monitor/status", "crying level 4")
    #not wet and silent (not crying and not screaming) - happy
    #wet and silent  - level 1
    #wet and over 150 - level 2
    #wet and 300 - level 3
    #wet and over 500 - level 4


            