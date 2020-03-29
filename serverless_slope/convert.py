from io import BytesIO

import numpy as np
from imageio import imread, imwrite

BINS = [26.5, 29.5, 31.5, 34.5, 45.5, 50.5, 59.5]
COLORMAP = [[255, 255, 255, 0], [248, 253, 85, 255], [241, 184, 64, 255],
            [238, 128, 49, 255], [235, 51, 35, 255], [122, 41, 217, 255],
            [0, 38, 245, 255], [0, 0, 0, 255]]


def main():
    # load data
    with open('1606.png', 'rb') as f:
        buf = f.read()

    # Get slope data
    slope = get_slope(buf)

    # Apply colormap and convert to rgba
    rgba = apply_colormap(slope, bins=BINS, colormap=COLORMAP)

    new_buf = BytesIO()
    imwrite(new_buf, rgba, format='png-pil', optimize=True)

    new_buf.seek(0)
    return new_buf.read()


def get_slope(buf):
    arr = imread(buf)

    # https://github.com/tilezen/joerd/blob/0b86765156d0612d837548c2cf70376c43b3405c/joerd/output/normal.py#L176-L179
    # Note that because of rounding necessary to encode as 8-bit ints, the
    # unscaled vector lengths don't add up exactly to 1
    unscaled = (arr / 128) - 1

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
    return np.arccos(unscaled[:, :, 2]) * 180 / math.pi


def apply_colormap(slope, bins, colormap):
    # Bin data
    inds = np.digitize(slope, bins)

    # Apply colormap, one at a time
    split = [dict(enumerate(map(lambda x: x[i], colormap))) for i in range(4)]
    arrs = []
    for split_map in split:
        arrs.append(np.vectorize(split_map.get)(inds))

    return np.dstack(arrs)
