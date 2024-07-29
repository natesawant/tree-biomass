import math
from pathlib import Path
from tempfile import NamedTemporaryFile
import requests
from dotenv import dotenv_values
import logging

TILE_SIZE = 256


class GoogleTiles:
    def __init__(self, api_key, session_token=None):
        self.api_key = api_key

        if session_token:
            self.session_token = session_token
        else:
            self.session_token = GoogleTiles.generate_session(api_key)

    def generate_session(api_key):
        res = requests.post(
            url=f"https://tile.googleapis.com/v1/createSession?key={api_key}",
            json={
                "mapType": "satellite",
                "language": "en-US",
                "region": "US",
                "scale": "scaleFactor4x",
                "highDpi": "true",
                "imageFormat": "jpeg",
            },
        )

        res.raise_for_status()

        print(res.json())

        return res.json().get("session")

    def request_tile_coords(self, lat, lng, output_filename, zoom=15):
        x, y, zoom = GoogleTiles.fromLatLngToTileCoord(lat, lng, zoom)
        return self.request_tile_point(zoom, x, y, output_filename)

    def request_tile_point(self, zoom, x, y, output_filename: Path):
        assert zoom >= 0 and zoom <= 22

        # Construct the URL with session token and API key
        url = f"https://tile.googleapis.com/v1/2dtiles/{zoom}/{x}/{y}?session={self.session_token}&key={self.api_key}"

        # Send an HTTP GET request to download the tile
        response = requests.get(url, stream=True)

        print(response)

        # Check for successful response status code
        response.raise_for_status()

        with open(output_filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Tile downloaded successfully and saved to {output_filename}")

    def fromLatLngToPoint(lat, lng):
        mercator = -math.log(math.tan((0.25 + lat / 360) * math.pi))
        return (
            TILE_SIZE * (lng / 360 + 0.5),
            TILE_SIZE / 2 * (1 + mercator / math.pi),
        )

    def fromLatLngToTileCoord(lat, lng, zoom=15):
        x, y = GoogleTiles.fromLatLngToPoint(lat, lng)
        scale = pow(2, zoom)

        return (
            math.floor(x * scale / TILE_SIZE),
            math.floor(y * scale / TILE_SIZE),
            zoom,
        )


if __name__ == "__main__":
    config = dotenv_values(".env")

    tiles = GoogleTiles(config.get("TILES_API_KEY"))
    with NamedTemporaryFile(
        suffix=".png", mode="wb", dir="tmp", delete=False
    ) as input_file:
        # with open("tmp/test.png", mode="wb") as input_file:
        # input_filepath = Path("tmp") / "test.png"
        input_filepath = Path(input_file.name)
        # tiles.request_tile_point(15, 6294, 13288, input_filepath)
        tiles.request_tile_coords(-33.8688, 151.2093, input_filepath)
