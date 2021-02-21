#!/usr/bin/env ipython
import socket
import time
import threading
from datetime import datetime
import paho.mqtt.client as mqtt
import readline # optional, will allow Up/Down/History in the console
import code
from IPython import embed
from IPython.core.display import display, HTML
import sys
from pathlib import Path
import json
import logging
FORMAT = '[%(levelname)s] %(name) -12s %(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('')  # root handler

instructions = []
myid = f"botchat-{socket.gethostname()}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

client = None

def get_broker():
    file = Path("/etc/sre/autobot.conf")
    if file.exists():
        config = json.loads(file.read_text())
        ip = config['broker'].get('ip')
        port = config['broker'].get('port', 1883)
        return ip, port

def _send_topic(topic, payload=None):
    topic = f"_autobot/console/{myid}/" + topic
    client.publish(topic, payload=payload, qos=2)

def whereAreYou():
    print("Asking bots to tell where they are...")
    _send_topic('whereAreYou')

def on_connect(client, userdata, flags, reason, properties):
    client.subscribe(f"_autobot/console/{myid}/#")

def on_message(client, userdata, msg):
    try:
        if msg.topic.split("/")[-1] == 'answer':
            value = msg.payload.decode("utf-8")
            print(value)
    except Exception as ex:
        logger.error(ex)

def start_broker():
    global client
    client = mqtt.Client(
        client_id=myid,
        protocol=mqtt.MQTTv5
    )
    client.on_connect = on_connect
    client.on_message = on_message

    ip, port = get_broker()
    print(f"Connecting {ip}:{port}")
    client.connect(ip, port, 60)

    client.loop_forever()


t = threading.Thread(target=start_broker)
t.daemon = True
t.start()

instructions.append("  whereAreYou()")


if __name__ == '__main__':
    from IPython import get_ipython
    print("Commands:")
    for instruction in instructions:
        print(f"  - {instruction}")
    embed(banner1='')
