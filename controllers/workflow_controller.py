from flask import request, jsonify
from services.comfyui_service import ComfyUIService
from utils.workflow_utils import WorkflowUtils
import logging

logger = logging.getLogger(__name__)

class WorkflowController:
    def __init__(self):
        self.comfyui_service = ComfyUIService()
        self.workflow_utils = WorkflowUtils()
    
    def execute_workflow(self):
        """Execute custom workflow"""
        try:
            data = request.get_json()
            
            if not data or 'workflow' not in data:
                return {"error": "Workflow data is required"}, 400
            
            workflow = data['workflow']
            timeout = data.get('timeout', 300)
            
            # Validate workflow
            if not self.workflow_utils.validate_workflow(workflow):
                return {"error": "Invalid workflow format"}, 400
            
            # Execute workflow
            images = self.comfyui_service.generate_images(workflow, timeout)
            
            # Process results
            results = []
            for node_id, image_list in images.items():
                for i, image_data in enumerate(image_list):
                    filename = f"workflow_{node_id}_{i}.png"
                    filepath = self.file_utils.save_image(image_data, filename)
                    results.append({
                        "node_id": node_id,
                        "filename": filename,
                        "url": f"/api/v1/images/download/{filename}"
                    })
            
            return {
                "success": True,
                "message": "Workflow executed successfully",
                "results": results
            }, 200
            
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            return {"error": str(e)}, 500
    
    def get_queue_status(self):
        """Get ComfyUI queue status"""
        try:
            status = self.comfyui_service.get_queue_status()
            return {
                "success": True,
                "queue_status": status
            }, 200
            
        except Exception as e:
            logger.error(f"Error getting queue status: {e}")
            return {"error": str(e)}, 500