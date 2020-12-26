import os

def offline_context_generator():
    for item in os.scandir(os.path.join('static', 'js', 'dalme_helpers')):
        if item.is_file():
            yield {'helper_static': 'js/dalme_helpers/' + item.name}
