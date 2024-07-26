# tree-biomass

## Requirements

- Conda

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
