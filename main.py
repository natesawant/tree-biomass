import logging
from typing import Annotated
from fastapi.responses import FileResponse
from fastapi import FastAPI, File, Form, HTTPException
from pathlib import Path
from tempfile import NamedTemporaryFile
from dotenv import dotenv_values

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
        model_mask: Annotated[bytes | None, File()],
        csv_file: Annotated[bytes | None, File()]
):
    with NamedTemporaryFile(
        suffix=".png", delete=False
    ) as input_mask, NamedTemporaryFile(suffix=".png", delete=False) as output_mask:
        input_filepath = Path(input_mask.name)
        output_filepath = Path(output_mask.name)

        logging.debug(f"input: {input_filepath}")
        logging.debug(f"output: {output_filepath}")

        logging.info("Writing image data to temporary file")
        input_filepath.write_bytes(base_mask)
        output_filepath.write_bytes(model_mask)

        logging.info("Computing metrics")
        if processor_type == "detectree":
            utils.evaluation(input_filepath, output_filepath)
        elif processor_type == "deepforest":
            utils.evaluation(input_filepath, output_filepath)
        elif processor_type == "samgeo":
            utils.evaluation(input_filepath, output_filepath)
        else:
            logging.warning("processor_type not allowed")
            raise HTTPException(
                status_code=400,
                detail="processor_type must be one of 'samgeo', 'detectree', or 'deepforest'",
            )
    raise NotImplementedError()