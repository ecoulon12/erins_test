import paho.mqtt.client as mqtt
import time
from grovepi import *

# Set the LCD port (replace with the actual port number)
lcd_port = 2

# Connect the LCD to the port
setRGB(lcd_port, 0, 128, 64)

# MQTT topic to subscribe to
mqtt_topic = "rpi_commands"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Received MQTT message on topic {msg.topic}: {msg.payload.decode()}")

    # Check the received message and update the LCD accordingly
    if msg.payload.decode() == "turn_on_lullaby":
        turn_on_lullaby()

def turn_on_lullaby():
    print("Received command to turn on lullaby!")
    setRGB(lcd_port, 0, 255, 0)  # Set LCD color to green
    setText(lcd_port, "Lullaby ON")  # Display message on the LCD

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_start()

    while True:
        time.sleep(1)
