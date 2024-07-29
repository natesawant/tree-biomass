import math
import requests

TILE_SIZE = 256


class GoogleTiles:
    def __init__(self, api_key, session_token=None):
        self.api_key = api_key

        if session_token:
            self.session_token = session_token
        else:
            self.session_token = GoogleTiles.generate_session(api_key)

    def generate_session(api_key):
        res = requests.get(
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

        return res.json().get("session")

    def request_tile_coords(self, lat, lng, zoom=15):
        return self.request_tile_coords(zoom, GoogleTiles.fromLatLngToPoint(lat, lng))

    def request_tile_point(self, zoom, x, y, output_filename):
        assert zoom >= 0 and zoom <= 22

        # Construct the URL with session token and API key
        url = f"https://tile.googleapis.com/v1/2dtiles/{zoom}/{x}/{y}?session={self.session_token}&key={self.api_key}"

        # Send an HTTP GET request to download the tile
        response = requests.get(url, stream=True)

        # Check for successful response status code
        response.raise_for_status()

        # Open the output file in write-binary mode
        with open(output_filename, "bx") as f:
            # Write the downloaded data to the file chunk by chunk
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Tile downloaded successfully and saved to {output_filename}")

    def fromLatLngToPoint(lat, lng):
        mercator = -math.log(math.tan((0.25 + lat / 360) * math.pi))
        return (
            TILE_SIZE * (lng / 360 + 0.5),
            TILE_SIZE / 2 * (1 + mercator / math.pi),
        )
