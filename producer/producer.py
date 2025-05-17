import pika
import json
import os
import time
import random
from faker import Faker
from datetime import datetime
from models.transactions import Transaction

fake = Faker()

def get_rabbitmq_connection(queue_name: str):
    rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
    rabbit_user = os.getenv('RABBITMQ_USER', 'guest')
    rabbit_pass = os.getenv('RABBITMQ_PASS', 'guest')
    credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
    parameters = pika.ConnectionParameters(host=rabbit_host, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    return connection, channel

def create_fake_transaction():
    return Transaction(
        amount=round(random.uniform(5, 100), 2),
        currency=random.choice(['USD', 'EUR', 'GBP']),
        timestamp=datetime.utcnow(),
        status=random.choice(['pending', 'completed', 'failed']),
        transaction_id=str(fake.uuid4()),
    )

def main():
    queue_name = 'transactions'
    connection, channel = get_rabbitmq_connection(queue_name)
    print('[*] Producer started. Sending transactions...')
    try:
        while True:
            transaction = create_fake_transaction()
            message = transaction.json()
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            print(f'[x] Sent transaction: {transaction}')
            time.sleep(random.uniform(0.5, 2))
    except KeyboardInterrupt:
        print('[*] Stopping producer...')
    finally:
        connection.close()

if __name__ == '__main__':
    main()
