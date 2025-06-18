import websocket
import uuid
import json
import urllib.request
import urllib.parse
import logging
import time
from typing import Dict, Any, Optional, List
from config.config import Config

logger = logging.getLogger(__name__)

class ComfyUIService:
    def __init__(self, server_address: str = None):
        self.server_address = server_address or Config.COMFYUI_SERVER
        self.client_id = str(uuid.uuid4())
        self.ws = None
        
    def connect_websocket(self):
        """Establish WebSocket connection to ComfyUI"""
        try:
            self.ws = websocket.WebSocket()
            ws_url = f"ws://{self.server_address}/ws?clientId={self.client_id}"
            self.ws.connect(ws_url)
            logger.info(f"Connected to ComfyUI WebSocket: {ws_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to ComfyUI WebSocket: {e}")
            return False
    
    def disconnect_websocket(self):
        """Close WebSocket connection"""
        if self.ws:
            try:
                self.ws.close()
                logger.info("WebSocket connection closed")
            except Exception as e:
                logger.error(f"Error closing WebSocket: {e}")
    
    def queue_prompt(self, prompt: Dict[str, Any]) -> Dict[str, Any]:
        """Queue a prompt for processing"""
        try:
            payload = {"prompt": prompt, "client_id": self.client_id}
            data = json.dumps(payload).encode('utf-8')
            
            url = f"http://{self.server_address}/prompt"
            req = urllib.request.Request(url, data=data)
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read())
                logger.info(f"Prompt queued successfully: {result.get('prompt_id')}")
                return result
                
        except Exception as e:
            logger.error(f"Failed to queue prompt: {e}")
            raise Exception(f"Failed to queue prompt: {e}")
    
    def get_image(self, filename: str, subfolder: str = "", folder_type: str = "output") -> bytes:
        """Retrieve generated image"""
        try:
            data = {
                "filename": filename,
                "subfolder": subfolder,
                "type": folder_type
            }
            url_values = urllib.parse.urlencode(data)
            url = f"http://{self.server_address}/view?{url_values}"
            
            with urllib.request.urlopen(url) as response:
                return response.read()
                
        except Exception as e:
            logger.error(f"Failed to get image {filename}: {e}")
            raise Exception(f"Failed to get image: {e}")
    
    def get_history(self, prompt_id: str) -> Dict[str, Any]:
        """Get generation history for a prompt ID"""
        try:
            url = f"http://{self.server_address}/history/{prompt_id}"
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read())
        except Exception as e:
            logger.error(f"Failed to get history for {prompt_id}: {e}")
            raise Exception(f"Failed to get history: {e}")
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        try:
            url = f"http://{self.server_address}/queue"
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read())
        except Exception as e:
            logger.error(f"Failed to get queue status: {e}")
            raise Exception(f"Failed to get queue status: {e}")
    
    def generate_images(self, workflow: Dict[str, Any], timeout: int = 300) -> Dict[str, List[bytes]]:
        """Generate images using workflow"""
        if not self.connect_websocket():
            raise Exception("Failed to connect to ComfyUI WebSocket")
        
        try:
            # Queue the prompt
            result = self.queue_prompt(workflow)
            prompt_id = result['prompt_id']
            
            # Wait for completion
            output_images = {}
            start_time = time.time()
            
            while True:
                if time.time() - start_time > timeout:
                    raise Exception(f"Generation timeout after {timeout} seconds")
                
                try:
                    out = self.ws.recv()
                    if isinstance(out, str):
                        message = json.loads(out)
                        if message['type'] == 'executing':
                            data = message['data']
                            if data['node'] is None and data['prompt_id'] == prompt_id:
                                break
                except websocket.WebSocketTimeoutError:
                    continue
                except Exception as e:
                    logger.warning(f"WebSocket receive error: {e}")
                    continue
            
            # Get the generated images
            history = self.get_history(prompt_id)[prompt_id]
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                images_output = []
                if 'images' in node_output:
                    for image in node_output['images']:
                        image_data = self.get_image(
                            image['filename'],
                            image['subfolder'],
                            image['type']
                        )
                        images_output.append(image_data)
                output_images[node_id] = images_output
            
            return output_images
            
        finally:
            self.disconnect_websocket()
