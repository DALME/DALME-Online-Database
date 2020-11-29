import mimetypes
import urllib
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from dalme_app.models import Page


def SessionUpdate(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])
        result = []
        for key, value in data.items():
            if not value:
                try:
                    del request.session[key]
                    result.append({'key': key, 'result': 'deleted'})
                except KeyError:
                    result.append({'key': key, 'result': 'skipped - does not exist'})
            else:
                request.session[key] = value
                result.append({'key': key, 'result': f'new value: {value}'})

        return HttpResponse(result)


def HealthCheck(request):
    return HttpResponse(status=200)


def DownloadAttachment(request, path):
    path_tokens = path.split('/')
    original_filename = path_tokens.pop(-1)
    file_path = settings.MEDIA_URL + path
    with urllib.request.urlopen(file_path) as fp:
        response = HttpResponse(fp.read())
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    # response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding
    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        # filename_header = 'filename=%s' % original_filename.encode('utf-8')
        filename_header = 'filename=%s' % original_filename
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


def PageManifest(request, pk):
    context = {}
    page = Page.objects.get(pk=pk)
    context['page'] = page
    context['canvas'] = page.get_canvas()
    return render(request, 'dalme_app/page_manifest.html', context)
