import json
import pika
from faker import Faker
from mongoengine import connect
from models import Contact

# З'єднання з базою даних MongoDB
connect('contacts_db')

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)

# Генерація фейкових контактів та їх запис у базу даних
fake = Faker()

for _ in range(10):  # Генеруємо 10 контактів для прикладу
    full_name = fake.name()
    email = fake.email()
    contact = Contact(full_name=full_name, email=email)
    contact.save()

    # Публікація повідомлення у чергу з ObjectID створеного контакту
    message = {'contact_id': str(contact.id)}
    channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))

connection.close()
