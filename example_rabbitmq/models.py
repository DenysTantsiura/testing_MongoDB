from mongoengine import Document
from mongoengine.fields import (
    BooleanField,
    StringField
)


class Contact(Document):
    fullname = StringField()
    email = StringField()
    delivery_status = BooleanField(default=False)
    description = StringField()
    phone = StringField()
    desired_mode = StringField()
