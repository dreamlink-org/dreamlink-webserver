from boto3 import client
from os.path import join, exists
from os import unlink

from dreamlink.lib.root import root_directory
from dreamlink.config import store_strategy, store_s3_bucket_name

class LocalStorageStrategy():
    def __init__(self, storage_path):
        self.storage_root = join(root_directory, storage_path)

    def check_data(self, file_key) -> bool:
        store_path = join(self.storage_root, file_key)
        return exists(store_path)

    def get_data(self, file_key):
        store_path = join(self.storage_root, file_key)
        with open(store_path, "rb") as file:
            return file.read()

    def set_data(self, file_key, data):
        store_path = join(self.storage_root, file_key)
        with open(store_path, "wb") as file:
            file.write(data)

    def delete_data(self, file_key):
        store_path = join(self.storage_root, file_key)
        unlink(store_path)

class S3StorageStrategy():
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = client("s3")

    def check_data(self, file_key) -> bool:
        try:
            self.client.head_object(Bucket = self.bucket_name, Key = file_key)
            return True
        except self.client.exceptions.ClientError as err:
            if err.response["Error"]["Code"] == "404":
                return False
            raise

    def get_data(self, file_key):
        response = self.client.get_object(Bucket = self.bucket_name, Key = file_key)
        return response["Body"].read()

    def set_data(self, file_key, data):
        self.client.put_object(Bucket = self.bucket_name, Key = file_key, Body = data)

    def delete_data(self, file_key):
        self.client.delete_object(Bucket = self.bucket_name, Key = file_key)

if store_strategy == "local":
    strategy = LocalStorageStrategy("store")
else:
    strategy = S3StorageStrategy(store_s3_bucket_name)