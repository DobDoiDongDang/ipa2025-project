import pika
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("RABBITMQ_DEFAULT_USER")
pwd = os.getenv("RABBITMQ_DEFAULT_PASS")
print(user, pwd)
creds = pika.PlainCredentials(user, pwd)


def produce(host, body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, credentials=creds)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(
        queue="router_jobs", exchange="jobs", routing_key="check_interfaces"
    )
    channel.basic_publish(exchange="jobs", routing_key="check_interfaces", body=body)
    connection.close()


def produce_interface_config(host, body, task):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, credentials=creds)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(queue="router_jobs", exchange="jobs", routing_key=task)
    channel.basic_publish(exchange="jobs", routing_key=task, body=body)
    connection.close()


if __name__ == "__main__":
    produce("rabbitmq", "192.168.100.21")
