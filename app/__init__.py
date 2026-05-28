from flask import Flask
from .extensions import db, login_manager
from .socket_events import socketio

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, async_mode='threading', cors_allowed_origins='*')

    from .routes.auth import auth_bp
    from .routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
