#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import locale
import argparse

try:
    from docker import Client
except ImportError:
    print("Cannot import Docker API, is docker_py installed?", file=sys.stderr)
    sys.exit(1)

try:
    from StringIO import StringIO
except:
    from io import StringIO

# Pseudographics
ZERO, ONE, TWO, THREE = (
    u'   ',
    u'|  ',
    u'+- ',
    u'+- '
) if locale.getdefaultlocale()[1] != 'UTF-8' else (
    u'   ',
    u'│  ',
    u'└─ ',
    u'├─ '
)


class Docktree(object):

    def __init__(self):
        cli = Client(base_url='unix://var/run/docker.sock', version='auto')
        self.images = cli.images(all=True)

    def build_tree(self):
        def name(image):
            id, tag = image['Id'][0:12], image['RepoTags'][0]
            if tag == '<none>:<none>':
                return id
            return id + ' ' + tag

        def children(image_id):
            return [i for i in self.images if i['ParentId'] == image_id]

        def tree(root_id=''):
            return [(name(img), tree(img['Id'])) for img in children(root_id)]

        def draw_tree(tree, marks):
            for i, (img, chldrn) in enumerate(tree):
                for x in marks:
                    print(ONE if x else ZERO, end='', file=f)
                if i < len(tree) - 1:
                    print(THREE + img, file=f)
                    draw_tree(chldrn, marks + [1])
                else:
                    print(TWO + img, file=f)
                    draw_tree(chldrn, marks + [0])

        f = StringIO()
        draw_tree(tree(''), [])
        return f.getvalue()


def main():
    parser = argparse.ArgumentParser(
        prog='docktree',
        description='Display the local Docker images as a tree.'
    )
    args = parser.parse_args()
    print(Docktree().build_tree(), end='')


if __name__ == '__main__':
    main()
