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

def create_docs():
    """Створення документів."""
    result_one = db.cats.insert_one(  # в БД звертаємось до неіснуючої колекції cats і він автоматично створює її та заповнює
        {
            "name": "barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"],  # масив однотипних даних
        }
    )

    print(result_one.inserted_id)  # дивимося чи повернув він те що вставив

    result_many = db.cats.insert_many(
        [
            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
        ]
    )
    print(result_many.inserted_ids)


def show_doc():
    """Отримання документу одного."""
    result = db.cats.find_one({"_id": ObjectId("6406daa75e1d9819e032ec1c")})
    print(result)


def show_docs():
    """Отримання декількох документів."""
    result = db.cats.find({})  # повертає об'єкт-курсор
    for el in result:  # перебираємо в циклі курсор
        print(el)


def update_doc():
    """Оновлення документу."""
    db.cats.update_one({"name": "barsik"}, {"$set": {"age": 8}})
    result = db.cats.find_one({"name": "barsik"})
    print(result)


def remove_doc():
    """Видалення документів."""
    db.cats.delete_one({"name": "barsik"})
    result = db.cats.find_one({"name": "barsik"})
    print(result)


if __name__ == '__main__':
    # create_docs()
    # show_doc()
    # show_docs()
    # update_doc()
    # remove_doc()
    pass

# poetry add pymongo[srv,tls]
# srv - для розпарсерня рядка підключення при конекті в хмару; tls - шифрування, щоб міг на HTTPS стукатись;
# poetry add pymongo[snappy,gssapi,srv,tls]  # wo snappy,gssapi, is Ok; 

# ~/.local/lib/python3.10/site-packages/poetry/utils/env.py:
