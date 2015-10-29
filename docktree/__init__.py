#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import locale

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

images = []


def name(image):
    id, tag = image['Id'][0:12], image['RepoTags'][0]
    if tag == '<none>:<none>':
        return id
    return id + ' ' + tag


def children(image_id):
    return [i for i in images if i['ParentId'] == image_id]


def tree(root_id=''):
    return [(name(img), tree(img['Id']))
            for img in children(root_id)]


def display(tree, marks):
    for i, (img, chldrn) in enumerate(tree):
        for x in marks:
            print(ONE if x else ZERO, end='')
        if i < len(tree) - 1:
            print(THREE + img)
            display(chldrn, marks + [1])
        else:
            print(TWO + img)
            display(chldrn, marks + [0])


def main():
    global images
    cli = Client(base_url='unix://var/run/docker.sock', version='auto')
    images = cli.images(all=True)
    display(tree(''), [])


if __name__ == '__main__':
    main()
