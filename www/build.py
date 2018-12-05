from dotenv import load_dotenv
import os
import argparse
import re
from datetime import datetime
from distutils.dir_util import copy_tree
from data_page_builder import DataPageBuilder
from list_page_builder import ListPageBuilder
from all_list_pages_builder import AllListPagesBuilder
from all_data_pages_builder import AllDataPagesBuilder
from items_loader import ItemsLoader
from settings import BUILD_PATH

load_dotenv()
DIRNAME = os.path.dirname(__file__)

def create_tmp_directories():
    for dir_path in [BUILD_PATH, os.path.join(BUILD_PATH, "data")]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

def augment_items(items):
    for item in items:
        item["date_diffusion_lisible"] = datetime.utcfromtimestamp(int(item["date_diffusion"]/1000)).strftime('%d/%m/%Y')
        item["path"] = DataPageBuilder.path_for_data_page(item)
        if item.get("contenu_html"):
            item["contenu_html"] = re.subn(r"src=\"\/", "src=\"https://insee.fr/", item["contenu_html"])[0]
    return items

def copy_static_assets():
    copy_tree(
        os.path.join(DIRNAME, "static_assets"),
        os.path.join(BUILD_PATH)
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-cache', const=True, action='store_const')
    parser.add_argument('--only-data-id', type=int)
    args = parser.parse_args()
    create_tmp_directories()

    items_loader = ItemsLoader()

    if args.use_cache:
        items = items_loader.load_from_cache()
    else:
        items = items_loader.load_from_s3()

    items = augment_items(items)

    if args.only_data_id:
        item = next((i for i in items if i["insee_id"] == args.only_data_id))
        DataPageBuilder(item).build()
        print("rebuilt single data page %s" % item["insee_id"])
        copy_static_assets()
    else:
        AllListPagesBuilder(items).build()
        AllDataPagesBuilder(items).build()
        print("finished rebuilding %s data pages finished." % len(items))
        copy_static_assets()

def rebuild_all():
    create_tmp_directories()
    items_loader = ItemsLoader()
    items = items_loader.load_from_s3()
    items = augment_items(items)
    AllListPagesBuilder(items).build()
    AllDataPagesBuilder(items).build()
    print("finished rebuilding %s data pages finished." % len(items))
    copy_static_assets()
