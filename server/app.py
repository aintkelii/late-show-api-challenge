from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from server.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Import models and controllers after app and db initialization
with app.app_context():
    from server.models import guest, episode, appearance, user
    from server.controllers import guest_controller, episode_controller, appearance_controller, auth_controller

    # Register blueprints
    app.register_blueprint(auth_controller.auth_bp)
    app.register_blueprint(guest_controller.guest_bp)
    app.register_blueprint(episode_controller.episode_bp)
    app.register_blueprint(appearance_controller.appearance_bp)

if __name__ == '__main__':
    app.run(debug=True)