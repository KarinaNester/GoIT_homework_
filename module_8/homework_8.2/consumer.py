import pika
import json
from models import Contact
from mongoengine import connect

# З'єднання з базою даних MongoDB
connect('contacts_db')

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)

def send_email(contact_id):
    # Логіка надсилання email (заглушка)
    # Ваш код для надсилання email тут

    # Позначення контакту як відправленого
    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.is_sent = True
        contact.save()

def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    contact_id = message.get('contact_id')
    if contact_id:
        send_email(contact_id)
        print(f"Email sent for contact with ID: {contact_id}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback)

print(' [*] Waiting for email messages. To exit press CTRL+C')
channel.start_consuming()
