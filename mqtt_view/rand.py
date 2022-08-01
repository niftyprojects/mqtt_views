import argparse
import datetime
import logging
from urllib.parse import urlparse

from paho.mqtt import client as mqtt

topic: str = "random/value"

LOG_LEVEL = {
    "debug": logging.DEBUG,
    "warn": logging.WARN,
    "error": logging.ERROR,
    "info": logging.INFO,
}


def on_message(client: mqtt.Client, user_data, msg: mqtt.MQTTMessage):
    """Handle an incoming message."""
    timestamp = datetime.datetime.now()

    try:
        val = int(msg.payload)
        print(f'{timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")} Value {val}')
    except ValueError:
        logging.error(f"Got non-integer value '{val}'")


def on_connect(client: mqtt.Client, user_data, flags, rc: int):
    if rc == mqtt.MQTT_ERR_SUCCESS:
        client.subscribe(topic)


def client_params(url: str):
    loc = urlparse(url)

    host = loc.hostname
    port = loc.port if loc.port else 1883
    assert loc.scheme == "mqtt"

    return (host, port)


def main():
    parser = argparse.ArgumentParser(
        description="Displays random numbers from a MQTT broker."
    )
    parser.add_argument(
        "--log_level",
        help="Set the logging level. Default error",
        choices=LOG_LEVEL.keys(),
        default="warn",
    )
    parser.add_argument(
        "broker",
        default="mqtt://localhost",
        help="MQTT broker URL, default mqtt://localhost",
        nargs="?",
    )
    args = parser.parse_args()

    logging.basicConfig(level=LOG_LEVEL[args.log_level])

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    host, port = client_params(args.broker)
    client.connect(host, port)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
