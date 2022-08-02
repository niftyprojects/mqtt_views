import argparse
import datetime
import json
import logging
from urllib.parse import urlparse

from paho.mqtt import client as mqtt

topic: str = "random/stats"

LOG_LEVEL = {
    "debug": logging.DEBUG,
    "warn": logging.WARN,
    "error": logging.ERROR,
    "info": logging.INFO,
}

KNOWN_KEYS = ["1_min", "5_min", "30_min"]


def validate_message(msg):
    try:
        for k in KNOWN_KEYS:
            if k not in msg or not isinstance(msg[k], float):
                return False
        return True
    except RuntimeError:
        pass
    return False


def display_init():
    print("-" * 50)
    print(f'|{"Time":^21}| {"1 min":>6} | {"5 min":>6} | {"30 min":>6} |')
    print("-" * 50)
    print(f'| {"Waiting for data...":46} |')
    print("-" * 50)


def display_stats(vals):
    min_1 = f'{vals["1_min"]:.3}'
    min_5 = f'{vals["5_min"]:.3}'
    min_30 = f'{vals["30_min"]:.3}'
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\u001B[5A", end="", flush=True)
    print("-" * 50)
    print(f'|{"Time":^21}| {"1 min":>6} | {"5 min":>6} | {"30 min":>6} |')
    print("-" * 50)
    print(f"| {time} | {min_1:>6} | {min_5:>6} | {min_30:>6} |")
    print("-" * 50)


def on_message(client: mqtt.Client, user_data, msg: mqtt.MQTTMessage):
    """Handle an incoming message."""

    try:
        vals = json.loads(msg.payload)
        if validate_message(vals):
            display_stats(vals)
        else:
            logging.error(f"Message {msg.mid} has invalid format")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding message {msg.mid}: {str(e)}")


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
        display_init()
        client.loop_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
