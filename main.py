import logging
from typing import Annotated
from fastapi.responses import FileResponse
from fastapi import FastAPI, File, Form, HTTPException
from pathlib import Path
from tempfile import NamedTemporaryFile
from dotenv import dotenv_values
from PIL import Image

import bounding_box_mask
import utils
from processors.deepforest_processor import DeepForestProcessor
from processors.detectree_processor import DetecTreeProcessor
from processors.samgeo_processor import SamgeoProcessor
from tiles import GoogleTiles

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

config = dotenv_values(".env")

app = FastAPI()
detectree = DetecTreeProcessor()
deepforest = DeepForestProcessor()
samgeo = SamgeoProcessor()

tiles = GoogleTiles(config.get("TILES_API_KEY"))


@app.get("/health")
async def root():
    return {"message": "Healthy!"}


@app.post("/process")
async def process(
        image_data: Annotated[bytes, File()], processor_type: Annotated[str, Form()]
):
    with NamedTemporaryFile(
            suffix=".jpg", delete=False
    ) as input_file, NamedTemporaryFile(suffix=".tif", delete=False) as output_file:
        input_filepath = Path(input_file.name)
        output_filepath = Path(output_file.name)

        logging.debug(f"input: {input_filepath}")
        logging.debug(f"output: {output_filepath}")

        logging.info("Writing image data to temporary file")
        input_filepath.write_bytes(image_data)

        logging.info("Starting to process image using processor")
        if processor_type == "detectree":
            detectree.process(input_filepath, output_filepath)
        elif processor_type == "deepforest":
            deepforest.process(input_filepath, output_filepath)
        elif processor_type == "samgeo":
            samgeo.process(input_filepath, output_filepath)
        else:
            logging.warning("processor_type not allowed")
            raise HTTPException(
                status_code=400,
                detail="processor_type must be one of 'samgeo', 'detectree', or 'deepforest'",
            )

        return FileResponse(output_file.name)


@app.post("/evaluate")
async def evaluate(
        base_mask: Annotated[bytes, File()],
        model_mask: Annotated[bytes | None, File()] = None,
        csv_file: Annotated[bytes | None, File()] = None
):
    with (NamedTemporaryFile(suffix=".png", delete=False) as input_mask,
          NamedTemporaryFile(suffix=".png", delete=False) as model,
          NamedTemporaryFile(suffix=".csv", delete=False) as boxes,
          NamedTemporaryFile(suffix=".png", delete=False) as output_csv):
        input_filepath = Path(input_mask.name)
        model_filepath = Path(model.name)
        csv_boxes = Path(boxes.name)
        output_csv_filepath = Path(output_csv.name)

        logging.debug(f"input: {input_filepath}")
        logging.debug(f"output: {model_filepath}")
        logging.debug(f"output: {csv_boxes}")

        logging.info("Writing image data to temporary file")
        input_filepath.write_bytes(base_mask)
        model_filepath.write_bytes(model_mask)
        if csv_file is not None:
            csv_boxes.write_bytes(csv_file)

        logging.info("Computing metrics")
        if csv_file is not None:
            width, height = bounding_box_mask.get_image_dimensions(input_filepath)
            bounding_box_mask.create_image_from_csv(csv_boxes, output_csv_filepath, width, height)
            metrics = utils.evaluation(input_filepath, output_csv_filepath)
        else:
            metrics = utils.evaluation(input_filepath, model_filepath)

        accuracy, precision, recall, f1_score = metrics

        return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1_score": f1_score}
