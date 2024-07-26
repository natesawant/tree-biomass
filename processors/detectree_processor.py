from processors.abstract_processor import AbstractProcessor
import detectree as dtr


class DetecTreeProcessor(AbstractProcessor):
    def __init__(self):
        pass

    def process(self, input_filepath, output_filepath):
        dtr.Classifier().predict_img(
            img_filepath=input_filepath, output_filepath=output_filepath
        )
