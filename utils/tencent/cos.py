# -*- coding:utf-8 -*-

from qcloud_cos import CosConfig, CosS3Client
from django.conf import settings
from utils.encrypt import uid


def create_bucket(bucket, region='ap-chengdu'):

    config = CosConfig(Region=region, SecretId=settings.SECRET_ID, SecretKey=settings.SECRET_KEY)
    client = CosS3Client(config)

    client.create_bucket(
        Bucket=bucket,
        ACL='public-read',
    )


def upload_file(bucket, region, file_object, key):
    config = CosConfig(Region=region, SecretId=settings.SECRET_ID, SecretKey=settings.SECRET_KEY)
    client = CosS3Client(config)
    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_object,
        Key = key,
    )
    return 'https://{}.cos.{}.myqcloud.com/{}'.format(bucket, region, key)


