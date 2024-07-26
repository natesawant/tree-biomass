from processors.abstract_processor import AbstractProcessor
from deepforest import main
from deepforest import get_data
from PIL import Image


class DeepForestProcessor(AbstractProcessor):
    def __init__(self):
        self.model = main.deepforest()
        self.model.use_release()

    def process(self, input_filepath, output_filepath):
        sample_image_path = get_data(input_filepath)
        img = self.model.predict_image(path=sample_image_path, return_plot=True)
        output = Image.fromarray(img)
        output.save(output_filepath)
