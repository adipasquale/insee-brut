import os
import pystache
from settings import BUILD_PATH
import markdown2

DIRNAME = os.path.dirname(__file__)

class MarkdownPageBuilder():

    def __init__(self, page_name, renderer=None):
        self.page_name = page_name
        self.template_path = os.path.join(DIRNAME, 'templates', 'markdown_page.mustache')
        self.renderer = renderer if renderer is not None else pystache.Renderer()

    def build(self):
        md_path = os.path.join(DIRNAME, 'markdown_pages', "%s.md" % self.page_name)
        with open(md_path) as f:
            content = markdown2.markdown(f.read())
        rendered_html = self.renderer.render_path(
            self.template_path, {
                "content": content
            }
        )
        rendered_path = os.path.join(BUILD_PATH, "%s.html" % self.page_name)
        print("rendering %s" % rendered_path)
        file = open(rendered_path, 'w')
        file.write(rendered_html)
        file.close()
