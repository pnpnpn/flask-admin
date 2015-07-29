from flask import Flask, url_for, redirect, render_template, request
from models.user import User, Role
from flask.ext.security import Security, MongoEngineUserDatastore, login_required, current_user

from flask.ext.mongoengine import MongoEngine

from wtforms import form, fields, validators

import flask_admin
#import flask_login as login
from flask_admin.contrib.mongoengine import ModelView
from flask_admin import helpers

# Create application
app = Flask(__name__)

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

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.objects(email=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    email = fields.TextField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if User.objects(email=self.login.data):
            raise validators.ValidationError('Duplicate username')


# Initialize flask-login
#def init_login():
#    login_manager = login.LoginManager()
#    login_manager.setup_app(app)
#
#    # Create user loader function
#    @login_manager.user_loader
#    def load_user(user_id):
#        return User.objects(id=user_id).first()
#

# Create customized model view class
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()


# Create customized index view class
class MyAdminIndexView(flask_admin.AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated()


# Flask views
@app.route('/')
def index():
    return render_template('index.html', user=current_user)


@app.route('/login/', methods=('GET', 'POST'))
def login_view():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.get_user()
        login.login_user(user)
        return redirect(url_for('index'))

    return render_template('form.html', form=form)


@app.route('/register/', methods=('GET', 'POST'))
def register_view():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()

        form.populate_obj(user)
        user.save()

        login.login_user(user)
        return redirect(url_for('index'))

    return render_template('form.html', form=form)


@app.route('/logout/')
def logout_view():
    login.logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize flask-login
    #init_login()

    # Create admin
    admin = flask_admin.Admin(app, 'Example: Auth-Mongo', index_view=MyAdminIndexView())

    # Add view
    admin.add_view(MyModelView(User))

    # Start app
    app.run(debug=True)
