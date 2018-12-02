import os
import pystache
import math
from list_page_builder import ListPageBuilder

DIRNAME = os.path.dirname(__file__)

class AllListPagesBuilder:
    ITEMS_PER_PAGE = 50

    def __init__(self, items, renderer=None):
        self.items = items
        self.renderer = renderer if renderer is not None else pystache.Renderer()

    def build(self):
      last_page_num = math.floor(len(self.items) / self.ITEMS_PER_PAGE) + 1
      for page_num in range(1, last_page_num + 1):
        start = (page_num - 1) * self.ITEMS_PER_PAGE
        page_items = self.items[start:start + self.ITEMS_PER_PAGE]
        ListPageBuilder(page_num, page_items, last_page_num, renderer=self.renderer)
      print("finished rebuilding %s list pages." % last_page_num)
