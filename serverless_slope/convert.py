import math
from io import BytesIO

import numpy as np
from imageio import imread, imwrite

BINS = [26.5, 29.5, 31.5, 34.5, 45.5, 50.5, 59.5]
COLORMAP = [[255, 255, 255, 0], [248, 253, 85, 255], [241, 184, 64, 255],
            [238, 128, 49, 255], [235, 51, 35, 255], [122, 41, 217, 255],
            [0, 38, 245, 255], [0, 0, 0, 255]]


# https://github.com/tilezen/joerd/blob/0b86765156d0612d837548c2cf70376c43b3405c/joerd/output/normal.py#L26-L41
def _generate_mapping_table():
    table = []
    for i in range(0, 11):
        table.append(-11000 + i * 1000)
    table.append(-100)
    table.append(-50)
    table.append(-20)
    table.append(-10)
    table.append(-1)
    for i in range(0, 150):
        table.append(20 * i)
    for i in range(0, 60):
        table.append(3000 + 50 * i)
    for i in range(0, 29):
        table.append(6000 + 100 * i)
    return table


# Make a constant version of the table for reference.
HEIGHT_TABLE = _generate_mapping_table()


def get_elevation(h: int):
    if h == 255:
        h -= 1

    return HEIGHT_TABLE[255 - h]


def normals_to_colormap(buf: bytes, bins=BINS, colormap=COLORMAP) -> bytes:
    """Convert png of normals to png of colormap

    Args:
        - buf: png buffer

    Returns:
        - png buffer of created image
    """
    # Load png image to array
    arr = imread(buf)

    # Get slope data
    slope = get_slope(arr)

    # Get mask of areas below 0 elevation
    mask = below_sea_level_mask(arr[:, :, 3])

    # Apply colormap and convert to rgba
    rgba = apply_colormap(slope, mask, bins=bins, colormap=colormap)

    # Create buffer and fill with image
    new_buf = BytesIO()
    imwrite(new_buf, rgba.astype('uint8'), format='png-pil', optimize=True)

    new_buf.seek(0)
    return new_buf.read()


def get_slope(arr: np.array) -> np.array:
    """Compute slope array from 4d array of normals
    """
    # https://github.com/tilezen/joerd/blob/0b86765156d0612d837548c2cf70376c43b3405c/joerd/output/normal.py#L176-L179
    # Note that because of rounding necessary to encode as 8-bit ints, the
    # unscaled vector lengths don't add up exactly to 1
    unscaled_z = (arr[:, :, 2] / 128) - 1

    # To find the slope, you want the angle between the normal vector and a
    # vector straight up from a horizontal surface. Such a straight up vector is
    # <0, 0, 1>.
    # Then the angle between two vectors is defined as
    #
    # A · B = |A| * |B| * cos(angle)
    #
    # Since A and B are unit vectors, |A| and |B| are 1.
    # A · B where B is <0, 0, 1> is equal to the z coord of A.
    # Then just take the arccos to find the angle.
    #
    # Finally, this angle is in radians, so convert to degrees
    # https://stackoverflow.com/a/16669463
    return np.arccos(unscaled_z) * 180 / math.pi


def below_sea_level_mask(arr: np.array) -> np.array:
    """Create mask of pixels below sea level

    Args:
        - arr: array (256, 256) of quantized elevation values

    Returns:
        np.array (256, 256). True means <0 elevation
    """
    # Vectorize function
    vfunc = np.vectorize(get_elevation)

    # Find quantized elevations
    ele = vfunc(arr)

    # Create mask
    return ele >= 0


def apply_colormap(slope, mask, bins, colormap):
    # Bin data
    inds = np.digitize(slope, bins)

    # Apply colormap, one at a time
    split = [dict(enumerate(map(lambda x: x[i], colormap))) for i in range(4)]
    arrs = []
    for split_map in split:
        channel = np.vectorize(split_map.get)(inds)

        # Where the mask is True, set to 0
        # This includes all elevations <0
        np.putmask(channel, mask, 0)
        arrs.append(channel)

    return np.dstack(arrs)
