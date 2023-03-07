import pymongo  # pymongo is a driver
from pymongo import MongoClient 
from pymongo.server_api import ServerApi  # 


from authentication import get_password


mongodb_password = get_password()

#  full driver connection from Database Deployments:
client = pymongo.MongoClient(
    f'mongodb+srv://tdv:{mongodb_password}@cluster0.7ylfcax.mongodb.net/?retryWrites=true&w=majority',
    server_api=ServerApi('1'))
db = client.test


result_one = db.cats.insert_one(
    {
        "name": "barsik",
        "age": 3,
        "features": ["ходить в капці", "дає себе гладити", "рудий"],
    }
)

print(result_one.inserted_id)

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


# poetry add pymongo[srv,tls]
# srv - для розпарсерня рядка підключення при конекті в хмару; tls - шифрування, щоб міг на HTTPS стукатись;
# poetry add pymongo[snappy,gssapi,srv,tls]  # wo snappy,gssapi, is Ok; 

# ~/.local/lib/python3.10/site-packages/poetry/utils/env.py:
