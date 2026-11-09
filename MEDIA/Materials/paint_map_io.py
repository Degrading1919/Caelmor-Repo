"""Catalog and PNG checks shared by the hand-painted map tools."""
from pathlib import Path

import numpy as np
from PIL import Image

from build_library import catalog, png


def material_record(material_id):
    record = next((row for row in catalog() if row['id'] == material_id), None)
    if record is None:
        raise ValueError(f'Unknown catalog material ID: {material_id}')
    return record


def read_grayscale_png(path: Path):
    """Read stored grayscale values, including opaque neutral RGB(A) exports."""
    with Image.open(path) as image:
        if image.format != 'PNG' or image.width != image.height or image.width < 2:
            raise ValueError('Input must be a square PNG at least 2 pixels wide')
        if image.mode in ('I', 'I;16', 'I;16B') and 'transparency' not in image.info:
            return np.asarray(image, dtype=np.float32) / 65535
        pixels = np.asarray(image.convert('RGBA'))
        if np.any(pixels[:, :, 3] != 255):
            raise ValueError('Flatten transparency before deriving maps')
        value = pixels[:, :, 0]
        if np.any(value != pixels[:, :, 1]) or np.any(value != pixels[:, :, 2]):
            raise ValueError('Input must be grayscale (equal RGB channels)')
        return value.astype(np.float32) / 255


def write_map(path: Path, pixels):
    if path.suffix.lower() != '.png':
        raise ValueError('Output filename must end in .png')
    data = png(pixels)
    # Exclusive creation also prevents an accidental in-place write to the art.
    with path.open('xb') as output:
        output.write(data)
