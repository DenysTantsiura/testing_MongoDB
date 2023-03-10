import configparser

from mongoengine import connect
import pika
# from pika import BlockingChannel

from authentication import get_password


CONFIG_FILE = 'example_rabbitmq/config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)


def rabbitmq_channel() -> tuple:
    """Connect to cloud rabbitmq service and return connection and channel."""
    rabbitmq_user = config.get('RABBIT_DEV', 'user')
    rabbitmq_password = get_password(config.get('RABBIT_DEV', 'password'))
    rabbitmq_host = config.get('RABBIT_DEV', 'claster')
    rabbitmq_vhost = config.get('RABBIT_DEV', 'virtual_host')
    rabbitmq_port = config.get('RABBIT_DEV', 'port')

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)  # 'guest', 'guest'
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_host,
        virtual_host=rabbitmq_vhost,  
        port=rabbitmq_port,  # TLS 5671    5672
        credentials=credentials))
    channel = connection.channel()  # Декларуємо канал

    return connection, channel


def create_connection() -> connect:
    """Connect to cloud MongoDB (cluster on AtlasDB) and return connection."""
    mongo_user = config.get('DB_DEV', 'user')
    mongodb_pass = config.get('DB_DEV', 'password')
    mongodb_pass = get_password()
    db_name = config.get('DB_DEV', 'db_name')
    domain = config.get('DB_DEV', 'domain')

    # connect to cluster on AtlasDB with connection string
    connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

    return connect
