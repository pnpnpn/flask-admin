from mongoengine import *
from flask.ext.mongoengine import Document as FDocument
from flask.ext.security import UserMixin, RoleMixin


class Role(FDocument, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)

class User(FDocument, UserMixin):
    email = StringField(max_length=120, required=True, unique=True)
    password = StringField(max_length=64)
    roles = ListField(ReferenceField(Role), default=[])
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()

    ## Flask-Login integration
    #def is_authenticated(self):
    #    return True

    #def is_active(self):
    #    return True

    #def is_anonymous(self):
    #    return False

    #def get_id(self):
    #    return str(self.id)

    ## Required for administrative interface
    #def __unicode__(self):
    #    return self.email
