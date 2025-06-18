from flask import Blueprint
from controllers.image_controller import ImageController

image_bp = Blueprint('images', __name__)
image_controller = ImageController()

@image_bp.route('/generate', methods=['POST'])
def generate_image():
    return image_controller.generate_image()

@image_bp.route('/download/<filename>', methods=['GET'])
def download_image(filename):
    return image_controller.download_image(filename)

@image_bp.route('/list', methods=['GET'])
def list_images():
    return image_controller.list_images()