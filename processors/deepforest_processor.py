import pandas as pd
from processors.abstract_processor import AbstractProcessor
from deepforest import main
from deepforest import get_data
from PIL import Image


class DeepForestProcessor(AbstractProcessor):
    def __init__(self):
        self.model = main.deepforest()
        self.model.use_release()

    def process(self, input_filepath, output_filepath, return_image=False):
        sample_image_path = get_data(input_filepath)
        prediction = self.model.predict_image(path=sample_image_path, return_plot=return_image)
        if return_image:
            output = Image.fromarray(prediction)
            output.save(output_filepath)
        else:
            df = pd.DataFrame(prediction, columns=['xmin','ymin','xmax','ymax'])
            df.to_csv(output_filepath, index=False)
