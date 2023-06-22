from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """Media storage class."""

    location = 'media'
    file_overwrite = False
    default_acl = 'private'
    custom_domain = False
