#!/usr/bin/env python
from livereload import Server, shell
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--only-data-id', type=int)
    args = parser.parse_args()
    if args.only_data_id:
        build_args = "--use-cache --only-data-id %s" % args.only_data_id
    else:
        build_args = "--use-cache"

    server = Server()
    server.watch(
        'templates/*.mustache',
        shell('python3 build.py %s' % build_args, cwd='scripts')
    )
    server.watch(
        'scripts/*.py',
        shell('python3 build.py %s' % build_args, cwd='scripts')
    )
    server.watch(
        '/tmp/insee_brut.items.json',
        shell('python3 build.py %s' % build_args, cwd='scripts')
    )
    server.serve(root='./build/')
