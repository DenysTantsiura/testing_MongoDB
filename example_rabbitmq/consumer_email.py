import sys
import time

# export PYTHONPATH="${PYTHONPATH}:/1prj/testing_MongoDB/"
from connect import create_connection, rabbitmq_channel
from models import Contact


TYPE_OF_CONSUMER = 'email'

connection, channel = rabbitmq_channel()
# RabbitMQ завершує роботу(звичайно або аварійно)- забуває про черги та повідомлення,
# якщо не вказано прапор durable=True щодо черги
channel.queue_declare(queue=TYPE_OF_CONSUMER, durable=True)  # Декларуємо чергу
print(' [*] Waiting for messages. To exit press CTRL+C')


def sending_to_email(message: str) -> None:
    """Imitation sending to e-mail."""
    contacts = Contact.objects()
    for contact in contacts:
        if message.split(':')[1] == str(contact.id):
            time.sleep(1)
            contact.update(delivery_status=True)
            print(f'The message was sent to the address {contact.fullname} ({contact.email})')


def callback(ch, method, properties, body) -> None:  # параметри - з документації
    """
    Функція callback повинна обов'язково приймати 4 аргументи:
    :param ch: поточний канал комунікації (цей об'єкт може перервати цикл всередині start_consuming якщо потрібно);
    :param method: детальна інформація про повідомлення;
    :param properties: службова інформація про повідомлення;
    :param body: тіло повідомлення у форматі bytes рядка.
    :return: None
    """
    message = body.decode()  # receiving data (body.decode())
    print(f" [x] Received: {message}")
    sending_to_email(message)
    print(f" [x] Done: {method.delivery_tag}")  # дістаємо ТЕГ - яку задачу виконали
    ch.basic_ack(delivery_tag=method.delivery_tag)  # повертаємо delivery_tag назад для сповіщення яку задачу виконали
    # через базову відповідь у каналі


channel.basic_qos(prefetch_count=1)  # rabbitmq кидай по 1 задачі, поки я(costumer) не закінчу
channel.basic_consume(queue=TYPE_OF_CONSUMER, on_message_callback=callback)  # підключаємось до черги


if __name__ == '__main__':
    print(f'\tConsumer start working, type: {TYPE_OF_CONSUMER}\n')
    create_connection()
    try:
        channel.start_consuming()

    except KeyboardInterrupt:
        print("Interrupted! Bye!")
        sys.exit(0)
