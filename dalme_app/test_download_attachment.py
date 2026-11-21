from unittest import mock

from django.test import RequestFactory, SimpleTestCase

from dalme_app.views.other import DownloadAttachment

FIREFOX = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0'
CHROME = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
)
PATH = 'dalme/attachments/2020/09/Autorisation de publication été.pdf'


class DownloadAttachmentTestCase(SimpleTestCase):
    def download(self, user_agent):
        request = RequestFactory().get('/download/', HTTP_USER_AGENT=user_agent)
        remote = mock.MagicMock()
        remote.__enter__.return_value.read.return_value = b'%PDF-1.4'
        with mock.patch('dalme_app.views.other.urllib.request.urlopen', return_value=remote):
            return DownloadAttachment(request, PATH)

    def test_firefox_gets_the_file_with_an_rfc_2231_filename(self):
        response = self.download(FIREFOX)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'%PDF-1.4')
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(
            response['Content-Disposition'],
            "attachment; filename*=UTF-8''Autorisation%20de%20publication%20%C3%A9t%C3%A9.pdf",
        )

    def test_chrome_gets_the_file_with_a_plain_filename(self):
        response = self.download(CHROME)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename=Autorisation de publication été.pdf',
        )
