from flask import Blueprint
from controllers.workflow_controller import WorkflowController

workflow_bp = Blueprint('workflows', __name__)
workflow_controller = WorkflowController()

@workflow_bp.route('/execute', methods=['POST'])
def execute_workflow():
    return workflow_controller.execute_workflow()

@workflow_bp.route('/queue/status', methods=['GET'])
def get_queue_status():
    return workflow_controller.get_queue_status()