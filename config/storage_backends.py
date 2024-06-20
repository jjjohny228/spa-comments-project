from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    """
    Storage class for private files
    """

    location = 'media'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False