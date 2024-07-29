# tree-biomass

## Requirements

- Conda

## Running deepforest_app

Install any of the following dependencies that you are missing

```sh
pip install pillow
```

```sh
pip install gradio
```

```sh
pip install deepforest
```

Change conda environment
```sh
conda activate deepforest
```

Run deepforest_app
```sh
python deepforest_app.py
```


## Running the FastAPI endpoints

```sh
conda env create -f environment.yml
```

```sh
conda activate treebiomass
```

```sh
uvicorn main:app --reload
```

You can view the Swagger documentation for each endpoint at http://localhost:8000/docs
