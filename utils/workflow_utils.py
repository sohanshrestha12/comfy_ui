import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from config.config import Config

logger = logging.getLogger(__name__)

class WorkflowUtils:
    def __init__(self):
        self.default_workflow_path = Path(Config.DEFAULT_WORKFLOW_PATH)
    
    def load_default_workflow(self) -> Dict[str, Any]:
        """Load default workflow from JSON file"""
        try:
            if not self.default_workflow_path.exists():
                raise FileNotFoundError(f"Default workflow not found: {self.default_workflow_path}")
            
            with open(self.default_workflow_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Failed to load default workflow: {e}")
            raise
    
    def update_workflow_params(self, workflow: Dict[str, Any], **params) -> Dict[str, Any]:
        """Update workflow parameters"""
        try:
            # This is based on your original workflow structure
            # Adjust node IDs and parameter paths according to your actual workflow
            
            if 'positive_prompt' in params and '74' in workflow:
                workflow['74']['inputs']['text'] = params['positive_prompt']
            
            if 'negative_prompt' in params and '75' in workflow:
                workflow['75']['inputs']['text'] = params['negative_prompt']
            
            if 'seed' in params and '72' in workflow:
                workflow['72']['inputs']['seed'] = params['seed']
            
            # Add more parameter mappings as needed
            # Example for other common parameters:
            # if 'steps' in params and 'sampler_node_id' in workflow:
            #     workflow['sampler_node_id']['inputs']['steps'] = params['steps']
            
            return workflow
            
        except Exception as e:
            logger.error(f"Failed to update workflow parameters: {e}")
            raise
    
    def validate_workflow(self, workflow: Dict[str, Any]) -> bool:
        """Validate workflow structure"""
        try:
            # Basic validation - check if it's a dictionary with expected structure
            if not isinstance(workflow, dict):
                return False
            
            # Check if workflow has nodes (keys should be node IDs)
            if not workflow:
                return False
            
            # Validate each node has required structure
            for node_id, node_data in workflow.items():
                if not isinstance(node_data, dict):
                    return False
                
                if 'inputs' not in node_data:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Workflow validation error: {e}")
            return False