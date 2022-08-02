Viewers for MQTT random values and statistics

## Instalation

Clone the repository and run the following commands:

```bash
poetry install
```

## Usage

`mqtt_viewrandom` displays the random value published to *random/value* on the specified broker.

```console
usage: mqtt_viewrand [-h] [--log_level {debug,warn,error,info}] [broker]

Displays random numbers from a MQTT broker.

positional arguments:
  broker                MQTT broker URL, default mqtt://localhost

options:
  -h, --help            show this help message and exit
  --log_level {debug,warn,error,info}
                        Set the logging level. Default error
```

`mqtt_viewstats` displays the averages of the random values published to *random/stats* on the specified
broker. 

```console
usage: mqtt_viewstats [-h] [--log_level {debug,warn,error,info}] [broker]

Displays averages of the random numbers from a MQTT broker.

positional arguments:
  broker                MQTT broker URL, default mqtt://localhost

options:
  -h, --help            show this help message and exit
  --log_level {debug,warn,error,info}
                        Set the logging level. Default error
```

