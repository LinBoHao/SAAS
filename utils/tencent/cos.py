# -*- coding:utf-8 -*-

from qcloud_cos import CosConfig, CosS3Client
from django.conf import settings


def create_bucket(bucket, region='ap-chengdu'):

    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)

    client.create_bucket(
        Bucket=bucket,
        ACL='public-read',
    )
    cors_config = {
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'POST', 'HEAD', 'PUT', 'DELETE'],
                'AllowedHeader': '*',
                'ExposeHeader': '*',
                'MaxAgeSeconds': 500
            }
        ]
    }
    client.put_bucket_cors(
        Bucket=bucket,
        CORSConfiguration=cors_config
    )


def upload_file(bucket, region, file_object, key):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)
    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_object,
        Key = key,
    )
    return 'https://{}.cos.{}.myqcloud.com/{}'.format(bucket, region, key)


def delete_file(bucket, region, key):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)
    client.delete_object(
        Bucket=bucket,
        Key=key,
    )
    # return 'https://{}.cos.{}.myqcloud.com/{}'.format(bucket, region, key)


def delete_file_list(bucket, region, key_list):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)
    objects = {
        "Quiet": 'true',
        'Objects': key_list

    }
    client.delete_object(
        Bucket=bucket,
        Delete=objects,
        Key=''
    )


def credential(bucket, region, ):

    from sts.sts import Sts

    config = {
        'duration_seconds': 180,
        'secret_id': settings.TENCENT_SECRET_ID,
        'secret_key': settings.TENCENT_SECRET_KEY,
        'bucket': bucket,
        'region': region,
        'allow_prefix': '*',
        'allow_actions': [
            # 'name/cos:PostObject',
            '*'
        ],
    }

    sts = Sts(config)
    result_dict = sts.get_credential()
    return result_dict


def check_file(bucket, region, key):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)
    response = client.head_object(
        Bucket=bucket,
        Key=key,
    )
    return response





