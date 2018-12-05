import os

TMP_PATH = os.path.join('/tmp', 'insee_brut')
BUILD_PATH = os.getenv("INSEE_BRUT_BUILD_PATH", TMP_PATH)
CACHE_PICKLE_PATH = os.path.join(TMP_PATH, 'items.pickle')
CACHE_JSON_PATH = os.path.join(TMP_PATH, 'items.json')