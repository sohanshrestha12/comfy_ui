import os
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration"""
    COMFYUI_SERVER = os.getenv('COMFYUI_SERVER', '127.0.0.1:8188')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', 'outputs')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # ComfyUI specific settings
    DEFAULT_WORKFLOW_PATH = os.getenv('DEFAULT_WORKFLOW_PATH', 'workflows/default.json')
    WEBSOCKET_TIMEOUT = int(os.getenv('WEBSOCKET_TIMEOUT', '300'))  # 5 minutes