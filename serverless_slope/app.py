from typing import BinaryIO, Tuple

from boto3.session import Session as boto3_session
from imageio import imread
from lambda_proxy.proxy import API

from serverless_slope.convert import normals_to_colormap
from serverless_slope.hillshade import hillshade
from serverless_slope.util import array_to_image

session = boto3_session()
s3_client = session.client("s3")

app = API(name="serverless-slope")


@app.route(
    "/slope/<int:z>/<int:x>/<int:y>.png",
    methods=["GET"],
    cors=True,
    payload_compression_method="gzip",
    binary_b64encode=True,
    tag=["tiles"])
def _img(z: int = None, x: int = None, y: int = None,
         **kwargs) -> Tuple[str, str, BinaryIO]:
    """Handle tile requests."""
    key = f'normal/{z}/{x}/{y}.png'
    obj = s3_client.get_object(Bucket='elevation-tiles-prod', Key=key)

    if obj['ResponseMetadata']['HTTPStatusCode'] != 200:
        return ("EMPTY", "text/plain", "empty tiles")

    normals = imread(obj['Body'].read())
    rgba = normals_to_colormap(normals)
    return ("OK", "image/png", array_to_image(rgba))


@app.route(
    "/hillshade/<int:z>/<int:x>/<int:y>.png",
    methods=["GET"],
    cors=True,
    payload_compression_method="gzip",
    binary_b64encode=True,
    tag=["tiles"])
def _img(z: int = None, x: int = None, y: int = None,
         **kwargs) -> Tuple[str, str, BinaryIO]:
    """Handle tile requests."""
    key = f'normal/{z}/{x}/{y}.png'
    obj = s3_client.get_object(Bucket='elevation-tiles-prod', Key=key)

    if obj['ResponseMetadata']['HTTPStatusCode'] != 200:
        return ("EMPTY", "text/plain", "empty tiles")

    normals = imread(obj['Body'].read())
    intensity = hillshade(normals, **kwargs)

    return ("OK", "image/png", array_to_image(intensity))


@app.route("/favicon.ico", methods=["GET"], cors=True, tag=["other"])
def favicon() -> Tuple[str, str, str]:
    """Favicon."""
    return ("EMPTY", "text/plain", "")
