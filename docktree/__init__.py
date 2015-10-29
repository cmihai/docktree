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


class Image(object):

    def __init__(self, img_dict):
        self.tags = [t for t in img_dict['RepoTags'] if t != '<none>:<none>']
        self.name = img_dict['Id'][0:12] + (' ' + ','.join(self.tags) if self.tags else '')
        self.children = []

    def matches(self, string):
        return string in self.name or any(string in t for t in self.tags)


class Docktree(object):

    def __init__(self, restrict='', file=sys.stdout):
        cli = Client(base_url='unix://var/run/docker.sock', version='auto')
        self.images = cli.images(all=True)
        self.restrict = restrict
        self.file = file

    def draw_tree(self):
        def children(image_id):
            return [i for i in self.images if i['ParentId'] == image_id]

        def tree(root_id=''):
            return [(Image(img_dict), tree(img_dict['Id'])) for img_dict in children(root_id)]

        def prune(branch):
            results = []
            for (image, children) in branch:
                if image.matches(self.restrict):
                    results.append((image, children))
                    continue
                children = prune(children)
                if children:
                    results.append((image, children))
            return results

        def draw_branch(branch, marks=[]):
            for i, (img, chldrn) in enumerate(branch):
                for x in marks:
                    print(ONE if x else ZERO, end='', file=self.file)
                if i < len(branch) - 1:
                    print(THREE + img.name, file=self.file)
                    draw_branch(chldrn, marks + [1])
                else:
                    print(TWO + img.name, file=self.file)
                    draw_branch(chldrn, marks + [0])

        draw_branch(prune(tree()))


def main():
    parser = argparse.ArgumentParser(
        prog='docktree',
        description='Display the local Docker images layers as a tree.'
    )
    parser.add_argument('image', metavar='IMAGE', nargs='?', help='show only parents and children of IMAGE')
    args = parser.parse_args()

    Docktree(restrict=args.image or '').draw_tree()


if __name__ == '__main__':
    main()
