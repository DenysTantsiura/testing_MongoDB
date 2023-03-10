from abc import ABC, abstractmethod
from typing import NoReturn, Optional
# from bson.objectid import ObjectId
import logging
from pprint import pprint
from timeit import default_timer

import pymongo  # pymongo is a driver
from pymongo.server_api import ServerApi

# export PYTHONPATH="${PYTHONPATH}:/1prj/testing_MongoDB/"
from authentication import get_password
from database.seed import upload_authors_to_the_database, upload_quotes_to_the_database
from database.models import Author, Quote
# import database.connect

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
name: <name>\tFind by Authors <name>.
tag: <tag>\tFind by <tag>.
tags: <tag>\tFind by <tags>.
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
        user_input = input(request)
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

'''
def command_handler(request: list) -> Optional[list]:
    """Main command handler - finder quotes."""
    match request[0]:  # python 3.10+
        case 'name':
            authors = [author.strip() for author in request[1:]]
            result = [Quote.objects(author=Author.objects(fullname__istartswith=author).first().id) for author in authors]
            
        case 'tag':
            tag = request[1].strip()
            result = [Quote.objects(tags__icontains=request[1])]
            
        case 'tags':
            tags = [tag.strip() for tag in request[1:]]
            # https://docs.mongoengine.org/guide/querying.html#string-queries
            result = [Quote.objects(tags__icontains=tag) for tag in tags]  
            
        case 'exit':
            result = None

        case _:
            result = []
            print('Unknown command!')

    result = ['0 found'] if result == [] else result

    return result
'''

class Quote_Finder():
    """Main quote finder class."""
    def __init__(self) -> None:
        print(f'{COMMAND_DESCRIPTION}\nYour request?\n')

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

    def search_by_author():
        return
    
    def search_by_tag():
        return
    
    @staticmethod
    def command_handler(request: list) -> Optional[list]:
        """Main command handler - finder quotes."""
        match request[0]:  # python 3.10+
            case 'name':
                authors = [author.strip() for author in request[1:]]
                result = [Quote.objects(author=Author.objects(fullname__istartswith=author).first().id) for author in authors]
                
            case 'tag':
                tag = request[1].strip()
                result = [Quote.objects(tags__icontains=request[1])]
                
            case 'tags':
                tags = [tag.strip() for tag in request[1:]]
                # https://docs.mongoengine.org/guide/querying.html#string-queries
                result = [Quote.objects(tags__icontains=tag) for tag in tags]  
                
            case 'exit':
                result = None

            case _:
                result = []
                print('Unknown command!')

        result = ['0 found'] if result == [] else result

        return result


def create_mongodb() -> None:
    "Створення хмарної бази даних Atlas MongoDB (quoters_book)."
    mongodb_password = get_password()
    #  full driver connection from Database Deployments:
    client = pymongo.MongoClient(
        f'mongodb+srv://tdv:{mongodb_password}@cluster0.7ylfcax.mongodb.net/?retryWrites=true&w=majority',
        server_api=ServerApi('1'))
    db = client.quoters_book  # звертаємось до неіснуючої БД quoters_book і вона автоматично створюється


def main():
    # Створіть хмарну базу даних Atlas MongoDB...
    create_mongodb()

    # Наповнення БД - завантаження json файлів у хмарну базу даних:
    if not Quote.objects():
        upload_authors_to_the_database()
        upload_quotes_to_the_database()

    # Пошук цитат за тегом, за ім'ям автора або набором тегів:
    Quote_Finder().start()


if __name__ == "__main__":
    main()
