import pika
import os


def produce(host, body):
    user = os.getenv("RABBITMQ_DEFAULT_USER")
    pwd = os.getenv("RABBITMQ_DEFAULT_PASS")
    creds = pika.PlainCredentials(user, pwd)
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


if __name__ == "__main__":
    produce("localhost", "192.168.1.44")
