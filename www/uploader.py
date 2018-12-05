import boto3
import os
from dotenv import load_dotenv
from settings import BUILD_PATH
# from gevent.pool import Pool
import threading
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

def upload_files():
    c = Counter()
    executor = ThreadPoolExecutor(max_workers=50)
    for subdir, dirs, files in os.walk(BUILD_PATH):
        for file in files:
            executor.submit(upload_file, file, subdir, c)

class Counter:
    counter = 0
    def increment(self, *args):
        self.counter += 1
        if self.counter % 10 == 0:
            print("uploaded %s" % self.counter)

def upload_file(file, subdir, c):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(os.getenv("AWS_S3_BUCKET_NAME_WWW"))
    full_path = os.path.join(subdir, file)
    with open(full_path, 'rb') as data:
        bucket.put_object(Key=full_path[len(BUILD_PATH)+1:], Body=data)
    c.increment()

if __name__ == "__main__":
    upload_files()
