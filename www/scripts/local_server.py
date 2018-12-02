#!/usr/bin/env python
from livereload import Server, shell
server = Server()
server.watch(
  '*.mustache',
  shell('python3 build.py --use-cache', cwd='scripts')
)
server.watch(
  'scripts/build.py',
  shell('python3 build.py --use-cache', cwd='scripts')
)
server.serve(root='./build/')
