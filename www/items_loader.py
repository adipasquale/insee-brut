import boto3
import botocore
import os
import pickle
import json
from settings import CACHE_PICKLE_PATH
from settings import CACHE_JSON_PATH

class ItemsLoader:

    def load_from_cache(self):
        if os.path.isfile(CACHE_JSON_PATH):
            with open(CACHE_JSON_PATH) as f:
                items = json.load(f, encoding='utf-8')
                print("%s items loaded from JSON cache" % len(items))
                return items
        elif os.path.isfile(CACHE_PICKLE_PATH):
            items = pickle.load(open(CACHE_PICKLE_PATH, "rb"))
            print("%s items loaded from pickle cache" % len(items))
            return items
        else:
            return self.load_from_s3()

    def load_from_s3(self):
        s3 = boto3.resource('s3')
        try:
            bucket = s3.Bucket(os.getenv("AWS_S3_BUCKET_NAME"))
            bucket.download_file(os.getenv("AWS_S3_FILE_NAME"), CACHE_JSON_PATH)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
        with open(CACHE_JSON_PATH) as f:
            items = json.loads(f.read())
        print("%s items were loaded from S3 json." % len(items))
        pickle.dump(items, open(CACHE_PICKLE_PATH, "wb"))
        return items