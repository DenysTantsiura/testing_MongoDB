import time
import json

import pika

from authentication import get_password


credentials = pika.PlainCredentials('ofavtdhc', get_password('key_rabbit.txt'))  # 'guest', 'guest'
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='cow.rmq2.cloudamqp.com', # claster: cow.rmq2.cloudamqp.com ; hosts: cow-01.rmq2.cloudamqp.com
    virtual_host='ofavtdhc',  
    port=5672,  # TLS 5671    5672
    credentials=credentials))
channel = connection.channel()  # Декларуємо канал

# RabbitMQ завершує роботу(звичайно або аварійно)- забуває про черги та повідомлення, якщо не вказано прапор durable=True щодо черги
channel.queue_declare(queue='task_queue', durable=True)  # Декларуємо чергу
print(' [*] Waiting for messages. To exit press CTRL+C')


'''
Функція callback повинна обов'язково приймати 4 аргументи:
ch — поточний канал комунікації (цей об'єкт може перервати виконання циклу всередині start_consuming якщо потрібно);
method — детальна інформація про повідомлення;
properties — службова інформація про повідомлення;
body — тіло повідомлення у форматі bytes рядка.
'''
def callback(ch, method, properties, body) -> None:  # параметри - з документації
    print(f"{ch},\n\n{method},\n\n{properties},\n\n{body}")
    message = json.loads(body.decode())  # receiving data (body.decode())
    print(f" [x] Received {message}")
    time.sleep(1)
    print(f" [x] Done: {method.delivery_tag}")  # дістаємо ТЕГ - яку задачу виконали
    ch.basic_ack(delivery_tag=method.delivery_tag)  # повертаємо delivery_tag назад для сповіщення яку задачу виконали
    # через базову відповідь у каналі


channel.basic_qos(prefetch_count=1)  # rabbitmq кидай по 1 задачі, поки я(costumer) не закінчу
channel.basic_consume(queue='task_queue', on_message_callback=callback)  #  підключаємось до черги


if __name__ == '__main__':
    channel.start_consuming()
