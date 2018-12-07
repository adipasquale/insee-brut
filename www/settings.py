import os
from dotenv import load_dotenv
load_dotenv()

TMP_PATH = os.path.join('/tmp', 'insee_brut')
BUILD_PATH = os.getenv("INSEE_BRUT_BUILD_PATH", TMP_PATH)
CACHE_PICKLE_PATH = os.path.join(TMP_PATH, 'items.pickle')
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.environ["MONGODB_DB_NAME"]
BOTTLE_DEBUG = os.getenv("BOTTLE_DEBUG", False)