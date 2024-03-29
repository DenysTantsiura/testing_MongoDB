import pika  # Для роботи з RabbitMQ в Python необхідно використовувати пакет
# https://customer.cloudamqp.com/instance/

# export PYTHONPATH="${PYTHONPATH}:/1prj/testing_MongoDB/"
from connect import rabbitmq_channel
from models import Contact
from seed import upload_contacts_to_the_database
from connect import create_connection


connection, channel = rabbitmq_channel()

channel.exchange_declare(exchange='task_exchange', exchange_type='direct')  # Декларуємо біржу свою


def main() -> None:
    contacts = Contact.objects()
    for contact in contacts:
        try:
            queue_type = str(contact.desired_mode)
            
        except Exception:
            queue_type = 'task_queue'

        # RabbitMQ завершує роботу(звичайно або аварійно) i -
        # забуває про черги та повідомлення, якщо не вказано прапор durable=True щодо черги
        channel.queue_declare(queue=queue_type, durable=True)  # Декларуємо чергу, якщо вже створена - то нічого
        channel.queue_bind(exchange='task_exchange', queue=queue_type)  # Біндимо(прив'язуємо) 
        channel.basic_publish(
            exchange='task_exchange',
            routing_key=str(contact.desired_mode),  # 'task_queue',
            body=f'Contact ID:{contact.id}',
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent to recipient by %r" % contact.id)  # !!!!!!!!

    connection.close()


if __name__ == '__main__':
    create_connection()

    if not Contact.objects():
        upload_contacts_to_the_database()

    main()
