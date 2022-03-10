from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
  location = 'static'
  default_acl = 'private'
  
class MediaStorage(S3Boto3Storage):
  bucket_name = 'cozymltd-bucket'
  location = 'staticfiles/images'
  file_overwrite = False