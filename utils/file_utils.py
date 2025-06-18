import os
from pathlib import Path
from typing import List, Dict, Any
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class FileUtils:
    def __init__(self):
        self.output_folder = Path(Config.OUTPUT_FOLDER)
        self.output_folder.mkdir(exist_ok=True)
    
    def save_image(self, image_data: bytes, filename: str) -> Path:
        """Save image data to file"""
        try:
            filepath = self.output_folder / filename
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            logger.info(f"Image saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save image {filename}: {e}")
            raise
    
    def get_image_path(self, filename: str) -> Path:
        """Get full path for image file"""
        return self.output_folder / filename
    
    def list_images(self) -> List[Dict[str, Any]]:
        """List all saved images"""
        try:
            images = []
            for filepath in self.output_folder.glob('*.png'):
                stat = filepath.stat()
                images.append({
                    "filename": filepath.name,
                    "size": stat.st_size,
                    "created": stat.st_ctime,
                    "url": f"/api/v1/images/download/{filepath.name}"
                })
            
            return sorted(images, key=lambda x: x['created'], reverse=True)
            
        except Exception as e:
            logger.error(f"Failed to list images: {e}")
            raise
    
    def delete_image(self, filename: str) -> bool:
        """Delete image file"""
        try:
            filepath = self.output_folder / filename
            if filepath.exists():
                filepath.unlink()
                logger.info(f"Image deleted: {filepath}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete image {filename}: {e}")
            return False