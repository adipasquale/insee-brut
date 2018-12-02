from dotenv import load_dotenv
import boto3
import botocore
import os
import pickle
import argparse
import json
import pystache
import math
from datetime import datetime
from distutils.dir_util import copy_tree

load_dotenv()
DIRNAME = os.path.dirname(__file__)
CACHE_ITEMS_FILE_PATH = os.path.join(DIRNAME, '..', 'tmp', 'items.pickle')
ITEMS_PER_PAGE = 50

def download_items():
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
    print("%s items were fetched from S3 json." % len(items))
    pickle.dump(items, open(CACHE_ITEMS_FILE_PATH, "wb"))
    return items


def create_tmp_directories():
    for dir_name in ["tmp", "build", "build/data"]:
        path = os.path.join(DIRNAME, '..', dir_name)
        if not os.path.exists(path):
            os.makedirs(path)

def augment_items(items):
    for item in items:
        item["date_diffusion_lisible"] = datetime.utcfromtimestamp(int(item["date_diffusion"]/1000)).strftime('%d/%m/%Y')
        item["path"] = path_for_data_page(item)
    return items

def filename_for_page_num(page_num):
    if page_num == 1:
        return "index.html"
    else:
        return "list_page_%s.html" % page_num

def filename_for_data_page(item):
    return "%s.html" % item["insee_id"]

def path_for_data_page(item):
    return os.path.join('data', filename_for_data_page(item))

def rebuild_list_pages(items):
    template_path = os.path.join(DIRNAME, '..', 'list.mustache')
    renderer = pystache.Renderer()
    last_page_num = math.floor(len(items)/ITEMS_PER_PAGE) + 1
    first_page = {"num": 1, "path": filename_for_page_num(1)}
    last_page = {"num": last_page_num, "path": filename_for_page_num(last_page_num)}
    for page_num in range(1, last_page_num + 1):
        pages_before = [
            {"num": p, "path": filename_for_page_num(p)}
            for p in range(max(1,page_num-5), page_num)
        ]
        pages_after = [
            {"num": p, "path": filename_for_page_num(p)}
            for p in range(page_num+1, min(last_page_num, page_num+5))
        ]
        start = (page_num - 1) * ITEMS_PER_PAGE
        rendered_html = renderer.render_path(
            template_path, {
                "items": items[start:start + ITEMS_PER_PAGE],
                "page": page_num,
                "pages_before": pages_before,
                "pages_after": pages_after,
                "last_page": last_page if page_num < last_page_num else None,
                "first_page": first_page if page_num > 6 else None
            }
        )
        rendered_path = os.path.join(DIRNAME, '..', 'build', filename_for_page_num(page_num))
        file = open(rendered_path, 'w')
        file.write(rendered_html)
        file.close()
    print("finished rebuilding %s list pages finished." % last_page_num)

def rebuild_data_pages(items):
    template_path = os.path.join(DIRNAME, '..', 'data.mustache')
    renderer = pystache.Renderer()
    for item in items:
        rendered_html = renderer.render_path(
            template_path, {
                "item": item
            }
        )
        rendered_path = os.path.join(DIRNAME, '..', 'build', path_for_data_page(item))
        file = open(rendered_path, 'w')
        file.write(rendered_html)
        file.close()
    print("finished rebuilding %s data pages finished." % len(items))

def copy_static_assets():
    copy_tree(
        os.path.join(DIRNAME, "..", "static_assets"),
        os.path.join(DIRNAME, "..", "build")
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-cache', const=True, action='store_const')
    args = parser.parse_args()
    create_tmp_directories()

    if args.use_cache and os.path.isfile(CACHE_ITEMS_FILE_PATH):
        items = pickle.load(open(CACHE_ITEMS_FILE_PATH, "rb"))
        print("%s items loaded from cache" % len(items))
    else:
        items = download_items()
    items = augment_items(items)
    rebuild_list_pages(items)
    rebuild_data_pages(items)
    copy_static_assets()