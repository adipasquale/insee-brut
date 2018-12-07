#!/usr/bin/env python
from livereload import Server, shell
import build
import argparse
from settings import BUILD_PATH
from functools import partial
import subprocess

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--only-data-id', type=int)
    args = parser.parse_args()
    cmd = ["python3", "build.py", "--use-cache"]
    if args.only_data_id:
        cmd.append("--only-data-id %s" % args.only_data_id)

    def rebuild_all():
        print(subprocess.call(cmd))

    cmd_md = cmd.copy()
    cmd_md += ["--only-markdown-pages"]
    def rebuild_md():
        print(subprocess.call(cmd_md))

    server = Server()
    server.watch('templates/data.mustache', rebuild_all)
    server.watch('templates/list.mustache', rebuild_all)
    server.watch('templates/markdown_page.mustache', rebuild_md)
    server.watch('markdown_pages/*.md', rebuild_md)
    server.watch('*.py', rebuild_all)
    server.serve(root=BUILD_PATH)
