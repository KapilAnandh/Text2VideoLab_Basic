import os
import torch
import numpy as np
import imageio
from flask import Flask, request, jsonify, send_file
from diffusers import TextToVideoZeroPipeline

# Initialize Flask app
app = Flask(__name__)

# Load model once at startup
MODEL_ID = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading pipeline on {device} ...")
pipe = TextToVideoZeroPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
pipe = pipe.to(device)

try:
    pipe.enable_attention_slicing()
except Exception:
    pass

try:
    pipe.enable_xformers_memory_efficient_attention()
except Exception:
    pass


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Kapil's Text2Video Lab 🎥",
        "usage": "POST /generate with JSON { 'prompt': 'your text here', 'fps': 8 }"
    })


@app.route("/generate", methods=["POST"])
def generate_video():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in request JSON"}), 400

    prompt = data["prompt"]
    fps = int(data.get("fps", 8))  # default 8 fps
    out_path = "output.mp4"

    try:
        out = pipe(prompt)
        frames = getattr(out, "frames", None) or getattr(out, "images", None)
        if frames is None:
            return jsonify({"error": "Pipeline did not return frames"}), 500

        frames_uint8 = []
        for f in frames:
            arr = np.array(f)
            if arr.dtype != np.uint8:
                arr = (arr * 255).clip(0, 255).astype("uint8")
            frames_uint8.append(arr)

        imageio.mimsave(out_path, frames_uint8, fps=fps)
        return send_file(out_path, mimetype="video/mp4")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 1122))
    app.run(host="0.0.0.0", port=port)
