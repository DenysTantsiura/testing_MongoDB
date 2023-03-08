from abc import ABC, abstractmethod
import argparse
from functools import wraps
from bson.objectid import ObjectId


import pymongo  # pymongo is a driver
from pymongo import MongoClient 
from pymongo.server_api import ServerApi


# export PYTHONPATH="${PYTHONPATH}:/1prj/testing_MongoDB/"
from authentication import get_password


mongodb_password = get_password()

#  full driver connection from Database Deployments:
client = pymongo.MongoClient(
    f'mongodb+srv://tdv:{mongodb_password}@cluster0.7ylfcax.mongodb.net/?retryWrites=true&w=majority',
    server_api=ServerApi('1'))
db = client.book  # звертаємось до неіснуючої БД book і вона автоматично створюється


# prog - назва програми (за замовчуванням: os.path.basename(sys.argv[0]))
parser = argparse.ArgumentParser(
        description='Simple example for use MongoDB.',
        epilog=f'...'
    )
# parser.add_argument('-a', '--action', action='store_true', help='Choice of action: create, list, update, remove.')
# parser.add_argument('-a', '--action', type=str, help=': Choice of action: create, list, update, remove.')
# parser.add_argument('-id', '--id', type=int, help=': Choice of ID.')  # type=int,
parser.add_argument('-name:', '--name', type=str, help=': Find by Author.')
parser.add_argument('-tag:', '--tag', type=str, help=': Find by tag.')
parser.add_argument('-tags:', '--tags', type=str, nargs='+', help=': Find by tags.')  # nargs '+' збирає в список
parser.add_argument('-exit', '--exit', type=str, help=': exit from program.')

'''
# ArgumentParser аналізує аргументи за допомогою методу parse_args()
arguments = vars(parser.parse_args())  # автоматично визначатиме аргументи командного рядка з sys.argv
# vars() метод перетворює на словник об'єкт, dict не можемо бо це не приведення типів, а перетворення
'''

class InterfaceInput(ABC):

    @abstractmethod
    def listen(self, *args, **kwargs):
        ...


class InputToParser(InterfaceInput):

    @staticmethod
    def listen(request='How can I help you?\n'):
        """Get a user string - separate the command and parameters - 
        return it to the list, where the first element is the command, 
        the others are parameters.

            Parameters:
                request (str): String line for user request.

            Returns:
                list command of user input (list): list of commands (list of strings).
        """
        user_input = input(request)
        print(f'{user_input=}')
        # ArgumentParser аналізує аргументи за допомогою методу parse_args()
        arguments = vars(parser.parse_args())  # автоматично визначатиме аргументи командного рядка з sys.argv
        # vars() метод перетворює на словник об'єкт, dict не можемо бо це не приведення типів, а перетворення
        print(f'{arguments=}')
        
        return user_input.strip().split(' ')

# ----------------------------------------
# !!! next video 8-1 : 56 minnext  ... 1h
# -----------------------------------------

if __name__ == '__main__':
    
    while True:
        user_request = InputToParser.listen()

            # if user_request[0] in ALL_COMMAND_ADDRESSBOOK:  # dict of commands
            #     bot_answer_result = OutputAnswer.show_out(user_request, self.contact_dictionary, self.path_file)
            # else:
            #     user_request = ['command_guesser'] + user_request
            #     bot_answer_result = OutputAnswer.show_out(user_request, None, '')

            # if not bot_answer_result:
            #     break
        if user_request == 'exitt':
            break
