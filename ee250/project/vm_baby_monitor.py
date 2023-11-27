"""EE 250L Lab 04 Starter Code

Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("monitor/mode")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_press(key):
    print("key pressed!")
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == 'w':
        print("BABY_MODE")
        #send "w" character to rpi
        client.publish("monitor/mode", "BABY_MODE", 0, False)
    elif k == 'a':
        print("SELF_REG_MODE")
        # send "SELF_REG_MODE
        client.publish("monitor/mode", "SELF_REG_MODE", 0, False)

if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)