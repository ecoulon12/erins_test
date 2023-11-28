"""publisher baby monitor code. Run on VM. Not currently"""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("status/mode")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    if (str(msg.payload, "utf-8") == "crying"):
        print("currently crying :(")
    


def on_modeMsg(client, userdata, msg): # turn into on_modeMsg
    if str(msg.payload, "utf-8") == "crying":
        #set mode to baby monitor
        mode = 1
        print("baby is crying!")
        time.sleep(1)
    print(msg.payload)

if __name__ == '__main__':

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.message_callback_add("monitor/mode", on_modeMsg)
    client.loop_start()

    while True:
        time.sleep(1)
        # client.publish("monitor/mode", "BABY", 0, False)
        # time.sleep(2)
        # client.publish("monitor/mode", "SELFREG", 0, False)
