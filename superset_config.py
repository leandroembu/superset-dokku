import os
#---------------------------------------------------------
# Superset specific config
#---------------------------------------------------------
# ROW_LIMIT = 5000
SUPERSET_WORKERS = 8 # for it to work in heroku basic/hobby dynos increase as you like
SUPERSET_WEBSERVER_PORT = os.environ['PORT']
#---------------------------------------------------------
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY')

#---------------------------------------------------------
# Flask App Builder configuration
#---------------------------------------------------------
# Your App secret key
SECRET_KEY = os.environ['SUPERSET_SECRET_KEY']

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# Superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# Cache configuration
# "CACHE_TYPE": "RedisCache",
# "CACHE_REDIS_URL": os.environ.get("REDIS_URL")

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = CSRF_ENABLED = False
TALISMAN_ENABLED = False

# use inserted X-Forwarded-For/X-Forwarded-Proto headers
ENABLE_PROXY_FIX = True
SQLLAB_ASYNC_TIME_LIMIT_SEC = 300
SQLLAB_TIMEOUT = 300
SUPERSET_WEBSERVER_TIMEOUT = 300

# Custom configs for embedding superset
from flask_appbuilder.security.views import expose
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_appbuilder.security.manager import AUTH_REMOTE_USER
from flask import  redirect, request, flash
from flask_login import login_user

# Create a custom view to authenticate the user
AuthRemoteUserView=BaseSecurityManager.authremoteuserview
class CustomAuthUserView(AuthRemoteUserView):
    @expose('/login/')
    def login(self):
        token = request.args.get('token')
        next = request.args.get('next')
        sm = self.appbuilder.sm
        session = sm.get_session
        user = session.query(sm.user_model).filter_by(username='admin').first()
        if token == os.environ["SUPERSET_EMBED_TOKEN"]:
            login_user(user, remember=False, force=True)
            if (next is not None):
                return redirect(next)
            else:
                return redirect(self.appbuilder.get_url_for_index)
        else:
            flash('Unable to auto login', 'warning')
            return super(CustomAuthUserView,self).login()

# Create a custom Security manager that overrides the CustomAuthUserView
class CustomSecurityManager(SupersetSecurityManager):
    authremoteuserview = CustomAuthUserView

# Use our custom authenticator
CUSTOM_SECURITY_MANAGER = CustomSecurityManager

# User remote authentication
AUTH_TYPE = AUTH_REMOTE_USER
