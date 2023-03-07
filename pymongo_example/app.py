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


# !!! next video 8-1 : 54 minnext


if __name__ == '__main__':
    # ...()
    pass