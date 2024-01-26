# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from project.models import db
from flask_cors import CORS
from project.config import TestingConfig



def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(TestingConfig)
    flask_app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    flask_app.config['JWT_COOKIE_SECURE'] = True
    flask_app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    return flask_app
flask_app = create_app() #have it take in development from .env file :>
db.init_app(flask_app)
migrate = Migrate(flask_app, db)
# Don't need to create celery again here
from project.routes import bp
flask_app.register_blueprint(bp)
CORS(flask_app,origins=["http://localhost:3000"],supports_credentials=True)
# Initialize JWTManager with the Flask app

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=5001, debug=True)
