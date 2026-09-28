"""Local-only synthetic sensor publisher, never plant telemetry."""
import json
import os
import random
import time

import paho.mqtt.client as mqtt


def main():
    rng = random.Random(133)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="aquavigil-synthetic-publisher")
    while True:
        try:
            client.connect(os.getenv("MQTT_HOST", "mosquitto"), 1883, 30)
            client.loop_start()
            break
        except OSError:
            time.sleep(3)
    n = 0
    while True:
        n += 1
        record = {"timestamp": int(time.time()), "ph": round(7.2+rng.uniform(-.16,.16), 3),
                  "conductivity": round(650+rng.uniform(-48,48), 2),
                  "turbidity": round(.32+rng.uniform(-.08,.08), 3),
                  "chlorine": round(1.1+rng.uniform(-.14,.14), 3),
                  "salinity": round(.22+rng.uniform(-.025,.025), 3),
                  "temperature": round(24+rng.uniform(-.6,.6), 2),
                  "pressure": round(56+rng.uniform(-1.5,1.5), 2),
                  "flow": round(1100+rng.uniform(-80,80), 2),
                  "source": "SYNTHETIC MQTT DEMO"}
        if n % 20 == 0:
            record["turbidity"] = 1.45  # transparent, periodic exercise condition
        client.publish("aquavigil/demo/water", json.dumps(record), qos=1)
        print(f"SYNTHETIC MQTT | sample {n} | pH={record['ph']} turbidity={record['turbidity']}", flush=True)
        time.sleep(10)


if __name__ == "__main__":
    main()
