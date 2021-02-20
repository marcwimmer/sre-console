#!/usr/bin/env ipython
import socket
import threading
from datetime import datetime
import paho.mqtt.client as mqtt
import readline # optional, will allow Up/Down/History in the console
import code
from IPython import embed
from IPython.core.display import display, HTML
import sys

instructions = []
myid = f"botchat-{socket.gethostname()}-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


def whereAreYou():
    print("Asking bots to tell where they are...")

def on_message(client, userdata, msg):
    if not msg.topic.startswith(f"{myid}/"):
        return
    print(msg.payload)

def start_broker():
    client = mqtt.Client(
        client_id=myid,
        protocol=mqtt.MQTTv5
    )
    client.on_message = on_message

    client.connect(
        config['broker']['ip'],
        config['broker'].get('port', 1883),
    60)

    client.loop_forever()


t = threading.Thread(target=start_broker)
t.daemon = False
t.start()

instructions.append("  whererAreYou()")


if __name__ == '__main__':
    from IPython import get_ipython
    print("Commands:")
    for instruction in instructions:
        print(f"  - {instruction}")
    embed(banner1='')
