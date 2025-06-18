from flask import Flask
from flask_cors import CORS
from config.config import Config
from routes.image_routes import image_bp
from routes.workflow_routes import workflow_bp
from routes.health_routes import health_bp
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    app.register_blueprint(image_bp, url_prefix='/api/v1/images')
    app.register_blueprint(workflow_bp, url_prefix='/api/v1/workflows')
    app.register_blueprint(health_bp, url_prefix='/api/v1/health')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)