from random import choice

from faker import Faker

from models import Contact
from connect import create_connection


NUMBER_OF_CONTACTS = 8


def contacts_generator(quantity_of: int = NUMBER_OF_CONTACTS) -> tuple:  # -> generator ()
    """Generate fake contacts (quantity_of)."""
    fake_data = Faker('uk_UA')

    fake_contacts = [fake_data.name() for _ in range(quantity_of)]
    fake_emails = [fake_data.email() for _ in range(quantity_of)]
    fake_descriptions = [fake_data.text() for _ in range(quantity_of)]
    fake_phones = [fake_data.phone_number() for _ in range(quantity_of)]
    fake_desired_mode = [choice(['sms', 'email']) for _ in range(quantity_of)]

    return tuple([(  # tuple excessive
        fake_contacts[el],
        fake_emails[el],
        fake_descriptions[el],
        fake_phones[el],
        fake_desired_mode[el]
        ) for el in range(quantity_of)])  # (fake_contacts, fake_emails, fake_descriptions)


def upload_contacts_to_the_database() -> None:
    """Upload contacts to database."""
    contacts = contacts_generator()
    [Contact(
        fullname=contact,
        email=email,
        description=text,
        phone=phone,
        desired_mode=mode
        ).save()
        for contact, email, text, phone, mode in contacts]


if __name__ == "__main__":
    create_connection()
    if not Contact.objects():
        upload_contacts_to_the_database()
