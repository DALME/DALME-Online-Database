"""Define offline context for django compressor."""

import os
import pathlib


def offline_context_generator():
    """Generate context for 'compressor' when off-line."""
    for item in os.scandir(pathlib.Path('static/js/helpers')):
        if item.is_file():
            yield {'helper_static': 'js/helpers/' + item.name}
