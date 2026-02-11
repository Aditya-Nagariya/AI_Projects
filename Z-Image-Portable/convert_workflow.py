import json
from typing import Any

def convert_ui_to_api(ui_workflow: dict[str, Any]) -> dict[str, Any]:
    api_workflow: dict[str, Any] = {}
    
    # Create a mapping from link ID to source node and slot
    link_map: dict[int, tuple[str, int]] = {}
    for link in ui_workflow.get("links", []):
        # Link format: [id, source_node_id, source_slot_index, target_node_id, target_slot_index, type]
        link_id: int = link[0]
        source_node_id = str(link[1])
        source_slot_index: int = link[2]
        link_map[link_id] = (source_node_id, source_slot_index)

    node: dict[str, Any]
    for node in ui_workflow.get("nodes", []):
        node_id = str(node["id"])
        class_type = node["type"]
        
        # Build inputs dictionary
        inputs: dict[str, Any] = {}
        
        # Handle widget values (configuration parameters)
        if "widgets_values" in node:
            # We need to map widget values to input names. 
            # This is tricky without knowing the exact node definition, 
            # but for simple cases or if we assume order matches, we might need a lookup or just guess.
            # However, prompt format usually requires explicit key-value pairs.
            # In API format, 'inputs' contains both connection links AND widget values.
            
            # Since we don't have the node definitions loaded to know input names easily here,
            # this conversion is imperfect for widgets. 
            # BUT, we can try to look at 'widgets_values' and see if we can map them.
            # Actually, standard ComfyUI API defaults to using widget values if they align? 
            # No, API format usually needs explicit names.
            
            # Let's see if we can just use the provided inputs from the UI format for links at least.
           pass

        # Handle inputs (links)
        if "inputs" in node:
            node_inputs: list[dict[str, Any]] = node["inputs"]  # pyre-fixme[6]
            for input_spec in node_inputs:
                name: str = input_spec["name"]
                if input_spec.get("link"):
                    link_id = int(input_spec["link"])
                    if link_id in link_map:
                        source_id, source_slot = link_map[link_id]  # pyre-fixme[6]
                        inputs[name] = [source_id, source_slot]

        # Handle widgets - this is the hard part without node class info.
        # But looking at Z-Image-Workflow.json, we can manually map for this specific workflow.
        
        if class_type == "UNETLoader":
           inputs["unet_name"] = node["widgets_values"][0]
           inputs["weight_dtype"] = node["widgets_values"][1]
           
        elif class_type == "CLIPLoader":
           inputs["clip_name"] = node["widgets_values"][0]
           inputs["type"] = "stable_diffusion" # Default required by newer ComfyUI
           
        elif class_type == "VAELoader":
           inputs["vae_name"] = node["widgets_values"][0]
           
        elif class_type == "StylePromptEncoder //ZImagePowerNodes":
           # Widgets: category, style, text. (customization is force_input=True so it should be a link or default empty?)
           # Workflow has 3 values: ["photo", "None", "prompt..."]
           
           inputs["category"] = node["widgets_values"][0]
           inputs["style"] = node["widgets_values"][1]
           inputs["text"] = node["widgets_values"][2]
           
           # Missing Input Link Fix: The original workflow JSON is missing the link from CLIPLoader (Node 2) to this node.
           # We must manually add it here to satisfy the required 'clip' input.
           # Assuming CLIPLoader is Node 2 and it outputs CLIP at slot 0.
           if "clip" not in inputs:
               inputs["clip"] = ["2", 0]
           
        elif class_type == "EmptyZImageLatentImage //ZImagePowerNodes":
           # Widgets: landscape, ratio, size, batch_size
           inputs["landscape"] = node["widgets_values"][0]
           inputs["ratio"] = node["widgets_values"][1]
           inputs["size"] = node["widgets_values"][2]
           inputs["batch_size"] = node["widgets_values"][3]
           
        elif class_type == "ZSamplerTurbo //ZImagePowerNodes":
           # Widgets: seed, control (randomize), steps, denoise
           inputs["seed"] = node["widgets_values"][0]
           inputs["steps"] = node["widgets_values"][2]
           inputs["denoise"] = node["widgets_values"][3]
           
        elif class_type == "VAEDecode":
            # VAEDecode usually doesn't have widgets, just inputs.
            pass

        elif class_type == "SaveImage":
           inputs["filename_prefix"] = node["widgets_values"][0]
           
        # Add class_type and inputs to API workflow
        api_workflow[node_id] = {
            "class_type": class_type,
            "inputs": inputs
        }
        
    return api_workflow

if __name__ == "__main__":
    import os
    try:
        with open("Z-Image-Workflow.json", "r") as f:
            ui_workflow = json.load(f)
        
        api_workflow = convert_ui_to_api(ui_workflow)
        
        print(json.dumps(api_workflow, indent=2))
        
        with open("Z-Image-Workflow-API.json", "w") as f:
            json.dump(api_workflow, f, indent=2)
            print("Successfully converted to Z-Image-Workflow-API.json")

    except FileNotFoundError:
        print("Error: Z-Image-Workflow.json not found.")
    except Exception as e:
        print(f"Error converting workflow: {e}")
