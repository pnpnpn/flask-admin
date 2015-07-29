from mongoengine import *
from flask.ext.mongoengine import Document as FDocument
from flask.ext.security import UserMixin, RoleMixin


class Role(FDocument, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)

    def __str__(self):
        return self.name

class User(FDocument, UserMixin):
    email = StringField(max_length=120, required=True, unique=True)
    password = StringField(max_length=64)
    roles = ListField(ReferenceField(Role), default=[])
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
