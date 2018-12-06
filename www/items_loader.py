import os
import pymongo
import pickle
from settings import CACHE_PICKLE_PATH, MONGODB_URI, MONGODB_DB_NAME

class ItemsLoader:

    def __init__(self):
        self.db = pymongo.MongoClient(MONGODB_URI)[MONGODB_DB_NAME]

    def load_from_cache(self):
        if os.path.isfile(CACHE_PICKLE_PATH):
            items = pickle.load(open(CACHE_PICKLE_PATH, "rb"))
            print("%s items loaded from pickle cache" % len(items))
            return items
        else:
            return self.load_from_mongo()

    def load_from_mongo(self):
        cursor = self.db.insee_items.find({"_type": "Statistiques"}).sort("dateDiffusion", -1)
        items = [i for i in cursor]
        print("%s items were loaded from mongo." % len(items))
        pickle.dump(items, open(CACHE_PICKLE_PATH, "wb"))
        return items

    def load_root_items(self, use_cache=False):
        if use_cache:
            return self.load_from_cache()
        else:
            return self.load_from_mongo()