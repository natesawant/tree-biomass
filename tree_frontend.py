import os
from PIL import Image
import gradio as gr
from deepforest import main
import tempfile

model = main.deepforest()
model.use_release()


def convert_rgba_to_rgb_and_save(image):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_path = temp_file.name
        image.save(temp_path)

    return temp_path


def deepforest_process(px):
    img = Image.fromarray(px)

    temp_path = convert_rgba_to_rgb_and_save(img)

    processed_img = model.predict_tile(temp_path, return_plot=True, patch_size=300, patch_overlap=0.25)

    os.remove(temp_path)
    return processed_img


interface = gr.Interface(fn=deepforest_process,
                         inputs=gr.Image(type="numpy", label="Upload Image"),
                         outputs=gr.Image(label="Predicted Image"),
                         )

interface.launch()
