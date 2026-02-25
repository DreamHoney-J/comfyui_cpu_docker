import base64
import io
import requests
import torch
import numpy as np
from PIL import Image


class SimpleGrok2APIGen:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_base": ("STRING", {"multiline": False, "default": ""}),
                "api_key": ("STRING", {"multiline": False, "default": ""}),
                "prompt": ("STRING", {"multiline": True, "forceInput": True}),
                "model": ("STRING", {"multiline": False, "default": "grok-imagine-1.0"}),
                "n": ("INT", {"default": 1, "min": 1, "max": 10}),
                "size": (["1024x1024", "1792x1024", "1024x1792", "1280x720", "720x1280"],),
                "response_format": (["b64_json", "base64", "url"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "Grok2API_Simple"

    def generate_image(self, api_base, api_key, prompt, model, n, size, response_format):
        endpoint = api_base.rstrip("/") + "/v1/images/generations"
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": model,
            "prompt": prompt,
            "n": int(n),
            "size": size,
            "response_format": response_format,
        }

        resp = requests.post(endpoint, headers=headers, json=payload, timeout=300)
        resp.raise_for_status()
        result = resp.json()

        data = result.get("data") or []
        if not data:
            raise RuntimeError(f"Empty response data: {result}")

        first = data[0]

        if response_format == "url":
            img_url = first.get("url")
            if not img_url:
                raise RuntimeError(f"Missing url: {first}")
            img_resp = requests.get(img_url, timeout=300)
            img_resp.raise_for_status()
            img_bytes = img_resp.content
        elif response_format == "b64_json":
            b64 = first.get("b64_json")
            if not b64:
                raise RuntimeError(f"Missing b64_json: {first}")
            img_bytes = base64.b64decode(b64)
        elif response_format == "base64":
            b64 = first.get("base64")
            if not b64:
                raise RuntimeError(f"Missing base64: {first}")
            img_bytes = base64.b64decode(b64)
        else:
            raise RuntimeError(f"Unsupported response_format: {response_format}")

        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = np.array(img).astype(np.float32) / 255.0
        img = torch.from_numpy(img)[None,]
        return (img,)


NODE_CLASS_MAPPINGS = {
    "SimpleGrok2APIGen": SimpleGrok2APIGen
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleGrok2APIGen": "Grok2API Image Generator (OpenAI compat)"
}
