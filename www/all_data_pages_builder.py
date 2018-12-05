import os
import pystache
import math
from data_page_builder import DataPageBuilder

class AllDataPagesBuilder:

    def __init__(self, items, renderer=None):
        self.items = items
        self.renderer = renderer if renderer is not None else pystache.Renderer()

    def build(self):
        for item in self.items:
            DataPageBuilder(item, renderer=self.renderer).build()