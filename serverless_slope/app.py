"""cogeo_mosaic_tiler.handlers.app: handle request for cogeo-mosaic-tiler endpoints."""

from typing import BinaryIO, Tuple

from boto3.session import Session as boto3_session
from lambda_proxy.proxy import API

from serverless_slope.convert import normals_to_colormap

session = boto3_session()
s3_client = session.client("s3")

app = API(name="serverless-slope")


@app.route(
    "/<int:z>/<int:x>/<int:y>.png",
    methods=["GET"],
    cors=True,
    payload_compression_method="gzip",
    binary_b64encode=True,
    tag=["tiles"],
)
def _img(
        z: int = None,
        x: int = None,
        y: int = None,
) -> Tuple[str, str, BinaryIO]:
    """Handle tile requests."""
    key = f'normal/{z}/{x}/{y}.png'
    obj = s3_client.get_object(Bucket='elevation-tiles-prod', Key=key)

    if obj['ResponseMetadata']['HTTPStatusCode'] != 200:
        return ("EMPTY", "text/plain", "empty tiles")

    colormap_png = normals_to_colormap(obj['Body'].read())
    return ("OK", "image/png", colormap_png)


@app.route("/favicon.ico", methods=["GET"], cors=True, tag=["other"])
def favicon() -> Tuple[str, str, str]:
    """Favicon."""
    return ("EMPTY", "text/plain", "")
