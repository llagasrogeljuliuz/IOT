import threading
import json
from PyP100 import PyP100
import time
import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as paho
from paho import mqtt

class IoT:
    def __init__(self):
        self.status = None
        self.previous_status = None  # Add previous status tracking
        self.root = tk.Tk()
        self.root.title("LIN Com")
        self.root.resizable(False, False)

        # Create the main frame
        self.main = ttk.Frame(self.root, padding=10)
        self.main.grid(row=0, column=0, sticky='NSEW')

        # open config file
        with open("info.json") as file:
            data = json.load(file)

        # Replace with your plug IP and your Tapo account credentials:
        self.ip = data["ip"]
        self.username = data["username"]
        self.password = data["password"]

        self.p100 = PyP100.P100(self.ip, self.username, self.password)
        self.p100.handshake()  # Required to establish auth cookies
        self.p100.login()  # Generates AES key & IV

        if data['state'] == "On":
            self.p100.set_status(True)
        elif data['state'] == "Off":
            self.p100.set_status(False)

        # ==== Content ====
        content = ttk.LabelFrame(self.main, text="ON/OFF BUTTON", width=100)
        content.grid(row=0, column=0, padx=10, pady=10)
        self.button = ttk.Button(content, text="TURN ON", command=self.button_state)
        self.button.grid(row=0, column=0, padx=10, pady=10)

        self.mac_address = "my/test/topic"  # self.p100.getDeviceInfo()['mac']
        threading.Thread(target=self.device_info, daemon=True).start()

    def button_state(self):
        self.p100.toggleState()

    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def client_param(self):
        try:
            # Create MQTT client
            self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv311)
            self.client.on_connect = self.on_connect

            # Enable TLS
            self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

            # Set username and password
            self.client.username_pw_set("user1", "User1234")

            # Connect to HiveMQ Cloud
            self.client.connect("5c1e782f3c924391aecb3b50c3b6316d.s1.eu.hivemq.cloud", 8883)

            # Set callbacks
            self.client.on_subscribe = self.on_subscribe
            self.client.on_message = self.on_message
            self.client.on_publish = self.on_publish

            return True  # Everything succeeded

        except Exception as e:
            print(f"MQTT client setup failed: {e}")
            return False  # Something went wrong

    def device_info(self):
        while True:
            self.status = self.p100.get_status()

            # Only perform the operation if the state has changed
            if self.status != self.previous_status:
                if self.client_param():

                    # Update button text
                    if self.p100.get_status():
                        self.button.configure(text='TURN OFF')
                        self.client.publish(self.mac_address, payload="""{"deviceId":"Device 1","state":"On"}""", qos=1)
                        self.client.subscribe(self.mac_address, qos=1)
                    else:
                        self.button.configure(text='TURN ON')
                        self.client.publish(self.mac_address, payload="""{"deviceId":"Device 1","state":"Off"}""", qos=1)
                        self.client.subscribe(self.mac_address, qos=1)

                    # Load existing JSON
                    with open('info.json', 'r') as file:
                        content = json.load(file)

                    # Update the state in the JSON file
                    content['state'] = 'On' if self.status else 'Off'

                    # Write it back
                    with open('info.json', 'w') as file:
                        json.dump(content, file, indent=4)

                    # Update previous status to the current state
                    self.previous_status = self.status

            time.sleep(1)  # Add a small delay to prevent the loop from running too fast

if __name__ == "__main__":
    app = IoT()
    app.root.mainloop()
