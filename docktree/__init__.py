#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import locale
import argparse
import codecs

try:
    from docker import Client
except ImportError:
    print("Cannot import Docker API, is docker_py installed?", file=sys.stderr)
    sys.exit(1)

if sys.version_info < (3,):
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)


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


def size_string(byte_count):
    if byte_count < 1000:
        return '%d B' % byte_count
    for power, suffix in enumerate(['B', 'KB', 'MB', 'GB', 'TB']):
        if byte_count < 1000 ** (power + 1):
            return '%3.1f %s' % (byte_count / 1000 ** power, suffix)


class Image(object):

    def __init__(self, img_dict, show_size=False):
        self.tags = [t for t in img_dict['RepoTags'] if t != '<none>:<none>']
        self.id = img_dict['Id']
        self.short_name = img_dict['Id'][0:12]
        self.virtual_size = size_string(img_dict['VirtualSize'])
        self.children = []
        self.show_size = show_size

    @property
    def name(self):
        result = [
            self.short_name,
            ' (%s)' % self.virtual_size if self.show_size else '',
            (' ' + ','.join(self.tags) if self.tags else '')
        ]
        return ''.join(result)

    def matches(self, string):
        return self.id.find(string) == 0 or any(string in t for t in self.tags)


class Docktree(object):

    def __init__(self, restrict='', file=sys.stdout, show_size=False):
        cli = Client(base_url='unix://var/run/docker.sock', version='auto')
        self.images = cli.images(all=True)
        self.restrict = restrict
        self.file = file
        self.show_size = show_size

    def draw_tree(self):
        def children(image_id):
            return [i for i in self.images if i['ParentId'] == image_id]

        def tree(root_id=''):
            return [(Image(img_dict, self.show_size), tree(img_dict['Id'])) for img_dict in children(root_id)]

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
                    print(ONE if x else ZERO, end=u'', file=self.file)
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
    parser.add_argument('restrict', metavar='IMAGE', default='', nargs='?', help='show only parents and children of IMAGE')
    parser.add_argument('-s', '--show-size', action='store_true', help='show the virtual size of each layer')
    args = parser.parse_args()

    Docktree(**vars(args)).draw_tree()


if __name__ == '__main__':
    main()
