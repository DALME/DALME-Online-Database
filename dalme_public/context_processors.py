from datetime import datetime


def year(request):
    return {'year': datetime.now().year}
