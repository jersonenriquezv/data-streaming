import pika
import pymongo
import json
import os
from models.transactions import Transaction

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

def get_mongodb_collection():
    mongo_host = os.getenv('MONGO_HOST', 'localhost')
    mongo_user = os.getenv('MONGO_USER', 'admin')
    mongo_pass = os.getenv('MONGO_PASS', 'password')
    mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:27017/"
    client = pymongo.MongoClient(mongo_uri)
    db = client['transactions']
    collection = db['transactions']
    return collection

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        transaction = Transaction(**data)
        collection = callback.mongo_collection
        collection.insert_one(transaction.dict())
        print(f"[x] Stored transaction: {transaction}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[!] Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    queue_name = 'transactions'
    connection, channel = get_rabbitmq_connection(queue_name)
    mongo_collection = get_mongodb_collection()
    callback.mongo_collection = mongo_collection  # Attach collection to callback
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print("[*] Waiting for messages. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("[*] Stopping consumer...")
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    main()



