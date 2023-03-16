"""Customize file storage for Django."""
from django_tenants.utils import parse_tenant_config_path
from storages.backends.s3boto3 import S3ManifestStaticStorage

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

# from datetime import datetime, timedelta
# from urllib.parse import urlencode
# from django.utils.encoding import filepath_to_uri


class LocalStorage(ManifestStaticFilesStorage):
    """Local file system storage with S3 read fallbacks for development."""
    # TODO: Something like composition?
    # If exists, super if not use MediaStorage() instance?


class StaticStorage(S3ManifestStaticStorage):
    """Multitenant aware staticfiles storage class for S3."""

    default_acl = None
    file_overwrite = False
    custom_domain = False

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = parse_tenant_config_path('%s')
        return settings


class MediaStorage(S3ManifestStaticStorage):
    """Multitenant aware media files storage class for S3.

    Here we permit the handling of two stores for media files so that during
    development any uploaded content referenced in the database will still be
    resolvable.

    The procedure is just to check to see if an item exists in the primary
    storage (which is the filesystem on development and a bucket on staging)
    and use that if so (this item, therefore, would something that has been
    added by a developer). Otherwise we can fall back to reads from the
    production bucket and that way existing CMS content should always be
    available no matter the environment.

    # TODO: Describe how we make the prod bucket read only.

    """

    default_acl = None
    file_overwrite = False
    custom_domain = False

    # @property
    # def environment(self):
    #     return os.environ['ENV']

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = parse_tenant_config_path('%s')
        # settings.update({
        #     'alternate_bucket_name': setting('AWS_STORAGE_ALTERNATE_BUCKET_NAME'),
        #     'alternate_custom_domain': setting('AWS_S3_ALTERNATE_CUSTOM_DOMAIN'),
        # })
        return settings

    # TODO: https://github.com/jschneier/django-storages/blob/89ca5bc8e31095f4c9e8bdf851557e41c6364122/storages/backends/s3boto3.py#L561

#     def url(self, name, parameters=None, expire=None, http_method=None):
#         params = parameters.copy() if parameters else {}
#         if self.exists(name):
#             r = self._url(name, parameters=params, expire=expire, http_method=http_method)
#         else:
#             params['Bucket'] = self.alternate_bucket_name
#             return self._url(name, parameters=params, expire=expire, http_method=http_method)

#     def _url(self, name, parameters=None, expire=None, http_method=None):
#         """
#         Similar to super().url() except that it allows the caller to provide
#         an alternate bucket name in parameters['Bucket']
#         """
#         # Preserve the trailing slash after normalizing the path.
#         name = self._normalize_name(self._clean_name(name))
#         params = parameters.copy() if parameters else {}
#         if expire is None:
#             expire = self.querystring_expire

#         if self.custom_domain:
#             bucket_name = params.pop('Bucket', None)
#             if bucket_name is None or self.alternate_custom_domain is None:
#                 custom_domain = self.custom_domain
#             else:
#                 custom_domain = self.alternate_custom_domain
#
#             url = '{}//{}/{}{}'.format(
#                 self.url_protocol,
#                 custom_domain,
#                 filepath_to_uri(name),
#                 '?{}'.format(urlencode(params)) if params else '',
#             )

#             if self.querystring_auth and self.cloudfront_signer:
#                 expiration = datetime.utcnow() + timedelta(seconds=expire)
#                 return self.cloudfront_signer.generate_presigned_url(url, date_less_than=expiration)

#             return url

#         if params.get('Bucket') is None:
#             params['Bucket'] = self.bucket.name
#         params['Key'] = name
#         url = self.bucket.meta.client.generate_presigned_url('get_object', Params=params,
#                                                              ExpiresIn=expire, HttpMethod=http_method)
#         if self.querystring_auth:
#             return url
#
#         return self._strip_signing_parameters(url)
