import boto3
import botocore
import os
import pickle
import json

DIRNAME = os.path.dirname(__file__)
CACHE_ITEMS_FILE_PATH = os.path.join(DIRNAME, '..', 'tmp', 'items.pickle')

class ItemsLoader:

    def create_tmp_directories(self):
        for dir_name in ["tmp"]:
            path = os.path.join(DIRNAME, '..', dir_name)
            if not os.path.exists(path):
                os.makedirs(path)

    def load_from_cache(self):
        if os.path.isfile(CACHE_ITEMS_FILE_PATH):
            items = pickle.load(open(CACHE_ITEMS_FILE_PATH, "rb"))
            print("%s items loaded from cache" % len(items))
            return items
        else:
            return self.load_from_s3()

    def load_from_s3(self):
        self.create_tmp_directories()
        s3 = boto3.resource('s3')
        try:
            bucket = s3.Bucket(os.getenv("AWS_S3_BUCKET_NAME"))
            bucket.download_file(os.getenv("AWS_S3_FILE_NAME"), 'tmp/items.json')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
        with open('tmp/items.json') as f:
            items = json.loads(f.read())
        print("%s items were loaded from S3 json." % len(items))
        pickle.dump(items, open(CACHE_ITEMS_FILE_PATH, "wb"))
        return items