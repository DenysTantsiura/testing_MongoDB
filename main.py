from abc import ABC, abstractmethod
# from bson.objectid import ObjectId
import logging
from pprint import pprint
from typing import NoReturn, Optional

import pymongo  # pymongo is a driver
from pymongo.server_api import ServerApi
import redis
from redis_lru import RedisLRU

# export PYTHONPATH="${PYTHONPATH}:/1prj/testing_MongoDB/"
from authentication import get_password
from database.seed import upload_authors_to_the_database, upload_quotes_to_the_database
from database.models import Author, Quote


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')


class InterfaceInput(ABC):

    @abstractmethod
    def listen(self, *args, **kwargs):
        ...


class InterfaceOutput(ABC):

    @abstractmethod
    def show_out(self, *args, **kwargs):
        ...


COMMAND_DESCRIPTION = '''
name: <name>\tFind by Author(s) <name>. Case insensitive, the names must be separated by commas. Examples: 
    \tname: Albert Einstein
    \tname: steve, albert
tag: <tag>\tFind by <tag>. Case insensitive, the tags must be separated by commas. Examples:
    \ttag: LIVE
    \ttag: miracle,success
tags: <tag>\tFind by <tags>. Case sensitive, the tags must be separated by commas. 
    \tEvery tag in tags (list of values) provided is in query. Examples:
    \ttags: deep-thoughts,change
exit\tTerminate program.
'''


class InputToParser(InterfaceInput):

    @staticmethod
    def listen(request=f'Your request?\n'):
        """Get a user string - separate the command and parameters - 
        return it to the list, where the first element is the command, 
        the others are parameters.

            Parameters:
                request (str): String line for user request.

            Returns:
                list command of user input (list): list of commands (list of strings).
        """
        user_input = input(request).lower()
        user_input = user_input.strip().split(':')
        if len(user_input) > 1:
            user_input = [user_input[0]] + user_input[1].strip().split(',')
        # print(f'{user_input=}')
        
        return user_input


class OutputAnswer(InterfaceOutput):

    @staticmethod
    def show_out(answer: list) -> None:
        """Show answer for the user.
            
            Parameters:
                answer (list): List of QuerySet objects or one str('0 found').
        """
        if isinstance(answer[0], str):
            return print(answer[0])
        
        for el in answer:  # el is <class 'mongoengine.queryset.queryset.QuerySet'>
            [pprint(qo.to_mongo().to_dict()) for qo in el]  # qo is <Quote: Quote object>


class ExceptValidation(Exception):
    pass


class QuoteFinder:
    """Main quote finder class."""
    # https://dev.to/ramko9999/host-and-use-redis-for-free-51if
    # Redis connect (to connect.py? but @cache, ... but external get_password()...):
    client = redis.Redis(
            host='redis-12148.c135.eu-central-1-1.ec2.cloud.redislabs.com',
            port=12148,
            password=get_password('key_redis.txt'))
            
    cache = RedisLRU(client)
    
    def __init__(self) -> None:
        print(f'{COMMAND_DESCRIPTION}\n')

    def start(self) -> NoReturn:
        """The main function of launching a quote finder that recognize 
        the commands entered from the keyboard and respond according 
        to the command entered. Enter a command - get an answer.
        """
        while True:
            user_request = InputToParser.listen()
            try:
                result = self.command_handler(user_request)

            except (Exception, ExceptValidation) as err:
                print(err)
                result = ['0 found']

            if result:
                OutputAnswer.show_out(result)
                
            else:
                break

    @cache
    @staticmethod
    def search_by_author(author: str) -> Quote.objects:
        print('____ If you see the following message: Searching - the first time without cache! ____')
        return Quote.objects(author=Author.objects(fullname__istartswith=author).first().id)
    
    @cache
    @staticmethod
    def search_by_tag(tag: str) -> Quote.objects:
        print('____ If you see the following message: Searching - the first time without cache! ____')
        return Quote.objects(tags__icontains=tag)
    
    @classmethod
    def command_handler(cls, request: list) -> Optional[list]:
        """Main command handler - finder quotes."""
        match request[0]:  # python 3.10+
            case 'name':
                authors = [author.strip() for author in request[1:]]
                result = [QuoteFinder.search_by_author(author) for author in authors]
                
            case 'tag':
                # tag = request[1].strip()  # if only one! - first, and without cache
                # result = [Quote.objects(tags__icontains=tag)]
                tags = [tag.strip() for tag in request[1:]]
                result = [QuoteFinder.search_by_tag(tag) for tag in tags]
                
            case 'tags':
                tags = [tag.strip() for tag in request[1:]]
                # https://docs.mongoengine.org/guide/querying.html#string-queries
                result = [Quote.objects(tags__all=tags)]  
                
            case 'exit':
                result = None

            case _:
                result = []
                print('Unknown command!')

        result = ['0 found'] if result == [] else result

        return result  # Optional[List[Quote.objects]]


def create_mongodb() -> None:
    """Створення хмарної бази даних Atlas MongoDB (quoters_book)."""
    mongodb_password = get_password()
    #  full driver connection from Database Deployments:
    client = pymongo.MongoClient(
        f'mongodb+srv://tdv:{mongodb_password}@cluster0.7ylfcax.mongodb.net/?retryWrites=true&w=majority',
        server_api=ServerApi('1'))
    client.quoters_book  # звертаємось до неіснуючої БД quoters_book і вона автоматично створюється


def main():
    # Створіть хмарну базу даних Atlas MongoDB...
    create_mongodb()

    # Наповнення БД - завантаження json файлів у хмарну базу даних:
    if not Quote.objects():
        upload_authors_to_the_database()
        upload_quotes_to_the_database()

    # Пошук цитат за тегом, за ім'ям автора або набором тегів:
    QuoteFinder().start()


if __name__ == "__main__":
    main()
