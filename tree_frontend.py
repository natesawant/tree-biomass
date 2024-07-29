import PIL
from PIL import Image
import gradio as gr
from deepforest import main
import matplotlib.pyplot as plt
import numpy as np

model = main.deepforest()
model.use_release()


def deepforest_process(px):

    img = Image.fromarray(px)
    print(type(img))

    temp_path = "/tmp/uploaded_image.png"
    plt.imsave(temp_path, img)

    # rgba_image = PIL.Image.open(temp_path)
    # rgb_image = rgba_image.convert('RGB')
    #
    # temp_path2 = "/tmp/uploaded_image2.png"
    # plt.imsave(temp_path2, rgb_image)

    img = model.predict_tile(temp_path, return_plot = True, patch_size=300,patch_overlap=0.25)

    return img

interface = gr.Interface(fn=deepforest_process,
                     inputs=gr.Image(type="numpy", label="Upload Image"),
                     outputs=gr.Image(label="Predicted Image"),
                     )

interface.launch()