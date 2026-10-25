#!/usr/bin/env python3
"""Compare static 8-bit RGB/RGBA PNGs; not an artwork/runtime gate."""
import argparse
import hashlib
import io
import json
from pathlib import Path

from PIL import Image, ImageChops


def compare(source, readback):
    paths = [Path(source), Path(readback)]
    encoded = [path.read_bytes() for path in paths]
    images = []
    for path, data in zip(paths, encoded):
        with Image.open(io.BytesIO(data)) as image:
            # RGB/RGBA PNGs with 16-bit channels can be silently downconverted by Pillow.
            if (image.format != 'PNG' or image.mode not in ('RGB', 'RGBA')
                    or data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR'
                    or data[24] != 8 or getattr(image, 'n_frames', 1) != 1):
                raise ValueError(f'{path}: only single-frame 8-bit RGB/RGBA PNGs are supported')
            images.append(image.convert('RGBA'))
    same_size = images[0].size == images[1].size
    hashes = [hashlib.sha256(data).hexdigest() for data in encoded]
    result = {
        'encoded_sha256': {'source': hashes[0], 'readback': hashes[1]},
        'encoded_bytes_equal': encoded[0] == encoded[1],
        'dimensions': {'source': list(images[0].size), 'readback': list(images[1].size)},
        'dimensions_equal': same_size,
        'rgba_equal': False,
        'changed_pixels': None,
        'maximum_channel_difference': None,
        'scope': 'Single-frame 8-bit RGB/RGBA PNGs only. All RGBA values, including RGB under zero alpha; no color-management transform.',
        'runtime_verified': False,
    }
    if same_size:
        difference = ImageChops.difference(*images)
        channels = difference.split()
        maxima = [channel.getextrema()[1] for channel in channels]
        # RGBA getbbox() may ignore RGB-only changes when alpha difference is zero.
        any_channel = channels[0]
        for channel in channels[1:]:
            any_channel = ImageChops.lighter(any_channel, channel)
        changed = images[0].width * images[0].height - any_channel.histogram()[0]
        result.update(
            rgba_equal=changed == 0,
            changed_pixels=changed,
            maximum_channel_difference=dict(zip(('R', 'G', 'B', 'A'), maxima)),
        )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('readback', type=Path)
    args = parser.parse_args()
    try:
        result = compare(args.source, args.readback)
    except (OSError, ValueError) as exc:
        print(json.dumps({'error': str(exc), 'runtime_verified': False}))
        return 2
    print(json.dumps(result, indent=2))
    return int(not result['rgba_equal'])


if __name__ == '__main__':
    raise SystemExit(main())
