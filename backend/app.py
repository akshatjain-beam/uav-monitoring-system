# backend/app.py

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .routes import health_bp, drones_bp, tasks_bp, images_bp
from .models import db

migrate = Migrate()

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        app: The configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uav_monitoring.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate
    
    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app, origins=["http://localhost:5174", "http://127.0.0.1:5174"], resources={r'/*': {'origins': '*'}})

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(drones_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(images_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
