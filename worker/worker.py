import pika
import json
import os
import time
from get_router_data import get_int_data, get_routing_data
from config_router_interface import config_router_interface
from config_loopback import add_loopback_interface, delete_loopback_interface
from save_data import save_interface

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_QUEUE = "router_jobs"
user = os.getenv("RABBITMQ_DEFAULT_USER")
pwd = os.getenv("RABBITMQ_DEFAULT_PASS")


def callback(ch, method, properties, body):
    print("Got it queue :", body.decode())
    routing_key = str(method.routing_key)
    if routing_key == "config_interfaces":
        message_data = json.loads(body.decode())
        ip = message_data.get("ip")
        config_router_interface(ip, message_data.get("data"), message_data.get("_id"))
    elif routing_key == "del_loopback":
        message_data = json.loads(body.decode())
        ip = message_data.get("ip")
        delete_loopback_interface(ip, message_data.get("data"), message_data.get("_id"))
    elif routing_key == "add_loopback":
        message_data = json.loads(body.decode())
        ip = message_data.get("ip")
        add_loopback_interface(ip, message_data.get("data"), message_data.get("_id"))
    else:
        message_data = json.loads(body.decode())
        ip = message_data.get("ip")
        username = message_data.get("username")
        password = message_data.get("password")
        int_data = get_int_data(ip, username, password)
        routing_data = get_routing_data(ip, username, password)
        save_interface(ip, int_data, routing_data)
    print("Done (;")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def listening():
    while True:
        try:
            creds = pika.PlainCredentials(user, pwd)
            connect = pika.BlockingConnection(
                pika.ConnectionParameters(
                    RABBITMQ_HOST,
                    credentials=creds,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            channel = connect.channel()
            channel.queue_declare(queue=RABBITMQ_QUEUE)
            print("Connected to rabbitmq waiting for queue")
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Can't connect to Rabbitmq: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
        except pika.exceptions.StreamLostError as e:
            print(f"Stream lost: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Critical error: {e}")
            raise  # Re-raise unhandled exceptions


if __name__ == "__main__":
    INTERVAL = 15.0
    next_run = time.monotonic()
    count = 0

    while True:
        now = time.time()
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        ms = int((now % 1) * 1000)
        now_str_with_ms = f"{now_str}.{ms:03d}"
        print(f"[{now_str_with_ms}] run #{count}")
        listening()
        count += 1
        next_run += INTERVAL
        time.sleep(max(0.0, next_run - time.monotonic()))
