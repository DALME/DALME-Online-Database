import datetime


def year(request):  # noqa: ARG001
    """Return current year."""
    return {'year': datetime.datetime.now(tz=datetime.UTC).year}


def project(request):  # noqa: ARG001
    """Return project name."""
    return {'project': 'The Documentary Archaeology of Late Medieval Europe'}
