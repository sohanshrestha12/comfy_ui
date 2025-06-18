from flask import Blueprint, jsonify
from services.comfyui_service import ComfyUIService
import logging

health_bp = Blueprint('health', __name__)
logger = logging.getLogger(__name__)

@health_bp.route('/ping', methods=['GET'])
def ping():
    return {"status": "healthy", "message": "Server is running"}, 200

@health_bp.route('/comfyui', methods=['GET'])
def check_comfyui():
    try:
        service = ComfyUIService()
        status = service.get_queue_status()
        return {
            "status": "healthy",
            "comfyui_connected": True,
            "queue_info": status
        }, 200
    except Exception as e:
        logger.error(f"ComfyUI health check failed: {e}")
        return {
            "status": "unhealthy",
            "comfyui_connected": False,
            "error": str(e)
        }, 503
