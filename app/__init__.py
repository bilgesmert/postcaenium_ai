import os
from flask import Flask
from flask_cors import CORS

from config import config_by_name
from app.database import init_db
from app.routes import api_bp, pages_bp

def create_app():
    app = Flask(__name__)

    env = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config_by_name[env])
    
    CORS(app, origins=app.config["CORS_ORIGINS"])
    init_db(app)
    
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app