from scrapy.item import BaseItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

# cf https://stackoverflow.com/questions/5069416/scraping-data-without-having-to-explicitly-define-each-field-to-be-scraped

class Serie(dict, BaseItem):
    pass

class SerieLoader(ItemLoader):
    default_output_processor = TakeFirst()

class RootDocument(dict, BaseItem):
    pass

class RootDocumentLoader(ItemLoader):
    default_output_processor = TakeFirst()
