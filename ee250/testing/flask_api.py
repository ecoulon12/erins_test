from flask import Flask, jsonify, request
import paho.mqtt.publish as publish

app = Flask(__name__)

# Dummy data for demonstration
dummy_data = {
    "baby_status": "Sleeping",
    "lullaby_status": "Off"
}

# MQTT topic for sending commands to the Raspberry Pi
mqtt_topic = "rpi_commands"

# Render the website
@app.route("/")
def index():
    return jsonify(dummy_data)

# Endpoint to turn on the lullaby
@app.route("/turn-on-lullaby", methods=["POST"])
def turn_on_lullaby():
    # Simulate turning on the lullaby
    dummy_data["lullaby_status"] = "On"
    
    # Publish a command to the Raspberry Pi
    publish.single(mqtt_topic, "turn_on_lullaby", hostname="localhost")

    return jsonify({"message": "Lullaby turned on"})

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
