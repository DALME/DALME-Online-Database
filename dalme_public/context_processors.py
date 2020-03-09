from datetime import datetime


def year(request):
    return {'year': datetime.now().year}

def project(request):
    return {'project': 'The Documentary Archaeology of Late Medieval Europe'}
