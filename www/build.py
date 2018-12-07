import os
import argparse
import re
from datetime import datetime
from distutils.dir_util import copy_tree
from data_page_builder import DataPageBuilder
from list_page_builder import ListPageBuilder
from all_list_pages_builder import AllListPagesBuilder
from all_data_pages_builder import AllDataPagesBuilder
from all_markdown_pages_builder import AllMarkdownPagesBuilder
from root_items_augmenter import RootItemsAugmenter
from items_loader import ItemsLoader
from settings import TMP_PATH, BUILD_PATH

DIRNAME = os.path.dirname(__file__)

def create_tmp_directories():
    for dir_path in [TMP_PATH, BUILD_PATH, os.path.join(BUILD_PATH, "data")]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

def copy_static_assets():
    copy_tree(
        os.path.join(DIRNAME, "static_assets"),
        os.path.join(BUILD_PATH)
    )

def build(use_cache=None, only_data_id=None, only_markdown_pages=False):
    create_tmp_directories()
    if only_markdown_pages:
        AllMarkdownPagesBuilder().build()
        return
    items_loader = ItemsLoader()
    root_items = items_loader.load_root_items(use_cache=use_cache)
    root_items = RootItemsAugmenter(root_items).augment()
    if only_data_id:
        item = next((i for i in root_items if i["id"] == only_data_id))
        DataPageBuilder(item).build()
        print("rebuilt single data page %s" % item["id"])
        copy_static_assets()
    else:
        AllListPagesBuilder(root_items).build()
        AllDataPagesBuilder(root_items).build()
        AllMarkdownPagesBuilder().build()
        print("finished rebuilding %s data pages finished." % len(root_items))
        copy_static_assets()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-cache', const=True, action='store_const')
    parser.add_argument('--only-data-id', type=int)
    parser.add_argument('--only-markdown-pages', const=True, action='store_const')
    args = parser.parse_args()
    build(
        use_cache = args.use_cache,
        only_data_id=args.only_data_id,
        only_markdown_pages=args.only_markdown_pages
    )
