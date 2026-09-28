"""Optional MQTT ingestion and InfluxDB mirror for generated demo records."""
import json
import os
import threading
import time


def write_influx(record):
    if os.getenv("INFLUXDB_ENABLED") != "1":
        return
    try:
        from influxdb_client import InfluxDBClient, Point
        from influxdb_client.client.write_api import SYNCHRONOUS
        fields = {key: value for key, value in record.items() if key in
                  ("ph", "conductivity", "turbidity", "chlorine", "salinity", "temperature", "pressure", "flow")}
        with InfluxDBClient(url=os.getenv("INFLUXDB_URL", "http://influxdb:8086"),
                            token=os.getenv("INFLUXDB_TOKEN", ""), org="aquavigil-demo", timeout=3000) as client:
            point = Point("synthetic_water_quality").tag("origin", "local_simulator")
            for key, value in fields.items():
                point = point.field(key, float(value))
            client.write_api(write_options=SYNCHRONOUS).write(bucket="sensors", record=point)
    except Exception as exc:
        print(f"SIMULATOR | InfluxDB write unavailable: {exc}", flush=True)


def start(app):
    if os.getenv("MQTT_ENABLED") != "1":
        return

    def listen():
        import paho.mqtt.client as mqtt
        from .analyzer import analyze, digest
        from ..db import save_analysis
        from ..metrics import observe

        def on_message(client, userdata, message):
            try:
                record = json.loads(message.payload)
                if record.get("source") != "SYNTHETIC MQTT DEMO":
                    return
                payload = json.dumps([record]).encode()
                result = analyze(payload, "synthetic-mqtt.json")
                result["workspace_roles"] = ["quality", "desalination"]
                with app.app_context():
                    analysis_id = save_analysis("synthetic-mqtt.json", digest(payload), result)
                    observe(result)
                write_influx(record)
                print(f"SIMULATOR | MQTT sample stored as analysis #{analysis_id}", flush=True)
            except Exception as exc:
                print(f"SIMULATOR | rejected sample: {exc}", flush=True)

        while True:
            try:
                client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="aquavigil-readonly-consumer")
                client.on_message = on_message
                client.connect(os.getenv("MQTT_HOST", "mosquitto"), 1883, 30)
                client.subscribe("aquavigil/demo/water", qos=1)
                client.loop_forever()
            except Exception as exc:
                print(f"SIMULATOR | MQTT broker unavailable: {exc}", flush=True)
                time.sleep(3)

    threading.Thread(target=listen, daemon=True, name="aquavigil-synthetic-mqtt").start()
