from flask import Flask, url_for, redirect, render_template, request
from models.user import User, Role
from flask.ext.security import Security, MongoEngineUserDatastore, login_required, current_user
from flask_admin import helpers as admin_helpers

from flask.ext.mongoengine import MongoEngine

from wtforms import form, fields, validators

import flask_admin
from flask_admin.contrib.mongoengine import ModelView
from flask_admin import helpers

# Create application
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# MongoDB settings
app.config['MONGODB_SETTINGS'] = {'DB': 'test'}
app.config['DEBUG'] = True

db = MongoEngine()
db.init_app(app)


user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#@app.before_first_request
#def create_user():
#    user_datastore.create_user(email='user1', password='password')
#
#    admin_role = user_datastore.create_role(name='role1')
#    admin_user = user_datastore.create_user(email='admin1', password='password')
#    user_datastore.add_role_to_user(admin_user, admin_role)
#    admin_user.save()

# Create customized model view class
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()

# Flask views
@app.route('/')
def index():
    return render_template('index.html', user=current_user)


#@security.context_processor
#def security_context_processor():
#    return dict(
#        admin_base_template=flask_admin.base_template,
#        admin_view=flask_admin.index_view,
#        h=admin_helpers,
#    )

if __name__ == '__main__':
    admin = flask_admin.Admin(
        app,
        'Example: Auth', template_mode='bootstap3')

    # Add view
    admin.add_view(MyModelView(User))
    admin.add_view(MyModelView(Role))

    # Start app
    app.run(debug=True)
