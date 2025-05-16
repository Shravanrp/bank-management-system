from flask import Flask
from banksystem.routes.auth import auth_bp
from banksystem.routes.dashboard import dashboard_bp
from banksystem.routes.profile import profile_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    
    app.register_blueprint(profile_bp)
    return app
