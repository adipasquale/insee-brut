import os
import pystache
import re
from markdown_page_builder import MarkdownPageBuilder

DIRNAME = os.path.dirname(__file__)
MARKDOWN_PAGES_PATH = os.path.join(DIRNAME, "markdown_pages")

class AllMarkdownPagesBuilder:

    def __init__(self, renderer=None):
        self.renderer = renderer if renderer is not None else pystache.Renderer()

    def build(self):
        for path in os.listdir(MARKDOWN_PAGES_PATH):
            print("building for path %s" % path)
            page_basename = os.path.basename(path)
            page_name = re.match(r"(.*)\.md", page_basename).groups()[0]
            print("building for page_name %s" % page_name)
            MarkdownPageBuilder(page_name, renderer=self.renderer).build()