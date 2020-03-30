from io import BytesIO

from imageio import imwrite


def array_to_image(arr):
    new_buf = BytesIO()
    imwrite(new_buf, arr, format='png-pil', optimize=True)

    new_buf.seek(0)
    return new_buf.read()
