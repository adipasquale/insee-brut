import os
import pystache

DIRNAME = os.path.dirname(__file__)

class ListPageBuilder:

    ITEMS_PER_PAGE = 50

    @staticmethod
    def filename_for_list_page_num(page_num):
        if page_num == 1:
            return "index.html"
        else:
            return "list_page_%s.html" % page_num

    @staticmethod
    def page_num_to_object(page_num):
        return {
            "num": page_num,
            "path": ListPageBuilder.filename_for_list_page_num(page_num)
        }

    def __init__(self, page_num, items, last_page_num, renderer=None):
        self.page_num = page_num
        self.items = items
        self.last_page_num = last_page_num
        self.template_path = os.path.join(DIRNAME, '..', 'list.mustache')
        self.renderer = renderer if renderer is not None else pystache.Renderer()
        self.filename = ListPageBuilder.filename_for_list_page_num(self.page_num)

    def build(self):
        first_page = self.page_num_to_object(1)
        last_page = self.page_num_to_object(self.last_page_num)
        pages_before = [
            self.page_num_to_object(p)
            for p in range(max(1,self.page_num - 5), self.page_num)
        ]
        pages_after = [
            self.page_num_to_object(p)
            for p in range(self.page_num + 1, min(self.last_page_num, self.page_num + 5))
        ]
        rendered_html = self.renderer.render_path(
            self.template_path, {
                "items": self.items,
                "page": self.page_num,
                "pages_before": pages_before,
                "pages_after": pages_after,
                "last_page": last_page if self.page_num < self.last_page_num else None,
                "first_page": first_page if self.page_num > 6 else None
            }
        )
        rendered_path = os.path.join(DIRNAME, '..', 'build', self.filename)
        file = open(rendered_path, 'w')
        file.write(rendered_html)
        file.close()