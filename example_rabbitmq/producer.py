from datetime import datetime
import json

import pika  # Для роботи з RabbitMQ в Python необхідно використовувати пакет
# https://customer.cloudamqp.com/instance/

from authentication import get_password


credentials = pika.PlainCredentials('ofavtdhc', get_password('key_rabbit.txt'))  # 'guest', 'guest'
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='cow.rmq2.cloudamqp.com', # claster: cow.rmq2.cloudamqp.com ; hosts: cow-01.rmq2.cloudamqp.com
    virtual_host='ofavtdhc',  
    port=5672,  # TLS 5671    5672
    credentials=credentials))
channel = connection.channel()  # Декларуємо канал


channel.exchange_declare(exchange='task_mock', exchange_type='direct')  # Декларуємо біржу свою
# RabbitMQ завершує роботу(звичайно або аварійно)- забуває про черги та повідомлення, якщо не вказано прапор durable=True щодо черги
channel.queue_declare(queue='task_queue', durable=True)  # Декларуємо чергу, якщо вже створена - то нічого
channel.queue_bind(exchange='task_mock', queue='task_queue')  # Біндимо(прив'язуємо) 


def main():
    for i in range(15):
        message = {
            "id": i + 1,
            "payload": f"Task #{i + 1}",
            "date": datetime.now().isoformat()
        }

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    main()
