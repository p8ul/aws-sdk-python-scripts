import os

try:
    import boto3
    from botocore.config import Config
except ImportError as e:
    raise ImportError("Could not load Boto3. %s" % e)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
BUCKET_NAME = os.getenv('BUCKET_NAME', '')
AWS_STORAGE_REGION = os.getenv('AWS_STORAGE_REGION', '')

AWS_CONFIG = Config(
    region_name=AWS_STORAGE_REGION,
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)


class AWS(object):
    def __init__(
            self, aws_config=AWS_CONFIG,
            bucket_name=BUCKET_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_storage_region=AWS_STORAGE_REGION, ):
        self._aws_config = aws_config
        self._bucket_name = bucket_name
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._aws_storage_region = aws_storage_region


class S3(AWS):
    OBJECT_NAME = 'S3'

    def __init__(self, *args, **kwargs):
        super(S3, self).__init__(*args, **kwargs)

        self.s3 = boto3.resource('s3', aws_access_key_id=self._aws_access_key_id,
                                 aws_secret_access_key=self._aws_secret_access_key)
        self.client = boto3.client('s3', aws_access_key_id=self._aws_access_key_id,
                                   aws_secret_access_key=self._aws_secret_access_key)
        self.download_target_dir = '/Users/paulkamita/projects/'
        # self.download_target_dir = '/home/bitnami/apps/wordpress/htdocs/'

    @classmethod
    def buckets(cls):
        return cls()._get_buckets()

    def _get_buckets(self):
        return [bucket for bucket in
                self.s3.Bucket(self._bucket_name).objects.filter(Prefix='site-backup/backup_2020-09')]

    @classmethod
    def download_file(cls, dir_name):
        return cls()._download_file(dir_name)

    def _download_file(self, dir_name):
        """
        Function to download files from an S3 bucket
        :param dir_name: bucket_name + folder to download directory e.g bucket_name/backup_folder
        :return: void
        """
        bucket = self.s3.Bucket(self._bucket_name)
        for obj in self.s3.Bucket(self._bucket_name).objects.filter(Prefix=dir_name):
            print('downloading', '..' * 13)
            file_dir = self.download_target_dir + obj.key
            if not os.path.exists(os.path.dirname(file_dir)):
                os.makedirs(os.path.dirname(file_dir))
            try:
                bucket.download_file(obj.key, file_dir)
            except:
                pass

    @classmethod
    def upload_file(cls, payload):
        return cls()._upload_file(payload)

    def _upload_file(self, payload):
        try:
            self.client.upload_fileobj(
                payload.get('data'),
                self._bucket_name,
                payload.get('file_name'),
                ExtraArgs={'ACL': 'public-read'}

            )
            return f"https://{self._bucket_name}.s3.amazonaws.com/{payload.get('data')}"
        except:
            return ''
