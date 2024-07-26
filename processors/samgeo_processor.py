from samgeo import tms_to_geotiff
from samgeo.text_sam import LangSAM
from processors.abstract_processor import AbstractProcessor
from utils import evaluation
from pathlib import Path


class SamgeoProcessor(AbstractProcessor):
    def __init__(self):
        self.sam = LangSAM()
        self.text_prompt = "tree"

    def process(self, input_filepath, output_filepath):
        self.sam.predict(
            str(input_filepath),
            self.text_prompt,
            box_threshold=0.10,
            text_threshold=0.05,
        )
        self.sam.show_anns(
            cmap="Greys_r",
            add_boxes=False,
            alpha=1,
            title="Automatic Segmentation of Trees",
            blend=False,
            output=str(output_filepath),
        )
