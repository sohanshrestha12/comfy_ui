import websocket 
import uuid
import json
import urllib.request
import urllib.parse

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break 
        else:
          
            continue 

    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        images_output = []
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
        output_images[node_id] = images_output

    return output_images

with open(r"E:\comfy\ComfyUI\script_examples\comfy_api\image_generator.json", "r", encoding = "utf-8") as f:
    workflow_jsonData = f.read()
    
jsonwf = json.loads(workflow_jsonData)
jsonwf["74"]["inputs"]["text"] = "mobile phone, smartphone, modern, high quality, detailed, realistic, 8k, product photography, studio lighting, white background"
jsonwf["75"]["inputs"]["text"] = "ugly, deformed, embedding:easynegative, nsfw, wings on head"




jsonwf["72"]["inputs"]["seed"] = 794599581709864

ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
images = get_images(ws, jsonwf)
for node_id, image_data in images.items():
    for i, img in enumerate(image_data):
        with open(f"output_{node_id}_{i}.png", "wb") as f:
            f.write(img)






ws.close() 

