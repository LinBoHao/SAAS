# -*- coding:utf-8 -*
from qcloud_cos import CosConfig, CosS3Client

from utils.tencent.cos import delete_file, delete_file_list

secret_id = 'AKIDlJgusZa9gwwa0Af6sNgqiFXYfXAWuuzt'
secret_key = 'w76ze8EBwUN6c1JF3En7GDyjHdlobGjz'

region = 'ap-chengdu'

config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key)

client = CosS3Client(config)

objects = {
    "Quiet": 'true',
    'Object': [
        {
            'Key': '1.png'
        },
        {
            'Key': '1.jpeg'
        }
    ]
}

client.delete_objects(
    Bucket='18830292815-1585297059-1252704499',
    Delete=objects
)

