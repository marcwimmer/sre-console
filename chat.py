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

myid = f"botchat-{socket.gethostname()}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

client = None

def chat(text, bot=None):
    if bot:
        text += "/" + bot
    _send_topic(text)

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

def on_connect(client, userdata, flags, reason, properties):
    client.subscribe(f"_autobot/console/{myid}/#")

def on_message(client, userdata, msg):
    try:
        if 'capabilities' in msg.topic.split("/"):
            print(f"Name: {msg.topic.split('/')[-1]}")
            print(msg.payload.decode('utf-8'))
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

while not client:
    time.sleep(0.1)


if __name__ == '__main__':
    from IPython import get_ipython
    print("Use chat('string') to communicate. Bots are now asks for what they understand.")
    print("To talk to a specific bot: chat('string', bot='botid'")
    _send_topic("ask_for_capabilities")
    embed(banner1='')
