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
    def rebuild():
        print(subprocess.call(cmd))
    server = Server()
    server.watch(
        'templates/*.mustache', rebuild
    )
    server.watch(
        '*.py', rebuild
    )
    server.serve(root=BUILD_PATH)
