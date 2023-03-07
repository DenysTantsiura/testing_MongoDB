import logging
# from time import time
from timeit import default_timer


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

# mongodb+srv://tdv:<password>@cluster0.7ylfcax.mongodb.net/?retryWrites=true&w=majority



def duration(fun):
    def inner(*args, **kwargs):
        start = default_timer()
        rez = fun(*args, **kwargs)
        logging.info(f'{default_timer()-start=} sec')

        return rez

    return inner


@duration
def main():
    print(default_timer())


if __name__ == "__main__":
    main()

# srv - для розпарсерня рядка підключення при конекті в хмару; tls - шифрування, щоб міг на HTTPS стукатись;
# poetry add pymongo[snappy,gssapi,srv,tls]  # wo snappy,gssapi, is Ok; 
