"""publisher baby monitor code. Run on VM. Not currently"""

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
        client.publish("monitor/mode", "BABY", 0, False)
    elif k == 'a':
        print("SELF_REG_MODE")
        # send "SELF_REG_MODE
        client.publish("monitor/mode", "SELFREG", 0, False)

def on_modeMsg(client, userdata, msg): # turn into on_modeMsg
    if str(msg.payload, "utf-8") == "crying":
        #set mode to baby monitor
        mode = 1
        print("baby is crying!")
        time.sleep(1)
    print(msg.payload)

    # elif str(msg.payload, "utf-8") == "happy":
    #     #set mode to self regulation
    #     mode = 2
    #     print("baby is happy")
    #     time.sleep(1)
    #print("message from monitor: ", msg.payload)

if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.message_callback_add("monitor/mode", on_modeMsg)
    client.loop_start()

    while True:
        time.sleep(1)
        client.publish("monitor/mode", "BABY", 0, False)
        time.sleep(2)
        client.publish("monitor/mode", "SELFREG", 0, False)
