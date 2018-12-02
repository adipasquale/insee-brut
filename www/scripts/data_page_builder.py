import os
import pystache

DIRNAME = os.path.dirname(__file__)

class DataPageBuilder():

    @staticmethod
    def filename_for_data_page(item):
        return "%s.html" % item["insee_id"]

    @staticmethod
    def path_for_data_page(item):
        return os.path.join('data', DataPageBuilder.filename_for_data_page(item))

    def __init__(self, item, renderer=None):
        self.item = item
        self.template_path = os.path.join(DIRNAME, '..', 'data.mustache')
        self.renderer = renderer if renderer is not None else pystache.Renderer()

    def build(self):
        rendered_html = self.renderer.render_path(
            self.template_path, {
                "item": self.item
            }
        )
        rendered_path = os.path.join(
            DIRNAME, '..', 'build',
            DataPageBuilder.path_for_data_page(self.item)
        )
        file = open(rendered_path, 'w')
        file.write(rendered_html)
        file.close()
