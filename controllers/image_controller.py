from flask import request, jsonify, send_file
from services.comfyui_service import ComfyUIService
from utils.workflow_utils import WorkflowUtils
from utils.file_utils import FileUtils
import json
import logging
import io
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ImageController:
    def __init__(self):
        self.comfyui_service = ComfyUIService()
        self.workflow_utils = WorkflowUtils()
        self.file_utils = FileUtils()
    
    def generate_image(self) -> Dict[str, Any]:
        """Generate image with custom prompt"""
        try:
            data = request.get_json()
            
            if not data:
                return {"error": "No JSON data provided"}, 400
            
            # Extract parameters
            positive_prompt = data.get('positive_prompt', '')
            negative_prompt = data.get('negative_prompt', '')
            seed = data.get('seed', -1)
            steps = data.get('steps', 20)
            cfg_scale = data.get('cfg_scale', 7.0)
            width = data.get('width', 512)
            height = data.get('height', 512)
            model_name = data.get('model_name', 'default')
            
            if not positive_prompt:
                return {"error": "positive_prompt is required"}, 400
            
            # Load and modify workflow
            workflow = self.workflow_utils.load_default_workflow()
            workflow = self.workflow_utils.update_workflow_params(
                workflow,
                positive_prompt=positive_prompt,
                negative_prompt=negative_prompt,
                seed=seed,
                steps=steps,
                cfg_scale=cfg_scale,
                width=width,
                height=height
            )
            
            # Generate images
            images = self.comfyui_service.generate_images(workflow)
            
            # Save images and prepare response
            saved_images = []
            for node_id, image_list in images.items():
                for i, image_data in enumerate(image_list):
                    filename = f"generated_{node_id}_{i}.png"
                    filepath = self.file_utils.save_image(image_data, filename)
                    saved_images.append({
                        "node_id": node_id,
                        "filename": filename,
                        "filepath": str(filepath),
                        "url": f"/api/v1/images/download/{filename}"
                    })
            
            return {
                "success": True,
                "message": "Images generated successfully",
                "images": saved_images,
                "parameters": {
                    "positive_prompt": positive_prompt,
                    "negative_prompt": negative_prompt,
                    "seed": seed,
                    "steps": steps,
                    "cfg_scale": cfg_scale,
                    "width": width,
                    "height": height
                }
            }, 200
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return {"error": str(e)}, 500
    
    def download_image(self, filename: str):
        """Download generated image"""
        try:
            filepath = self.file_utils.get_image_path(filename)
            if not filepath.exists():
                return {"error": "Image not found"}, 404
            
            return send_file(filepath, as_attachment=True)
            
        except Exception as e:
            logger.error(f"Error downloading image {filename}: {e}")
            return {"error": str(e)}, 500
    
    def list_images(self) -> Dict[str, Any]:
        """List all generated images"""
        try:
            images = self.file_utils.list_images()
            return {
                "success": True,
                "images": images
            }, 200
            
        except Exception as e:
            logger.error(f"Error listing images: {e}")
            return {"error": str(e)}, 500