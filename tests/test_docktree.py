#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sh
import os
import re
from os.path import dirname
from docktree import Docktree
try:
    from StringIO import StringIO
except:
    from io import StringIO


def setup_module():
    os.chdir(dirname(__file__))


def teardown_function(function):
    try:
        sh.docker('rmi', '-f', 'footest', 'bartest')
    except:
        pass


def test_single_image():
    sh.docker(sh.cat('empty.tar'), 'import', '-', 'footest')
    f = StringIO()
    Docktree(restrict='footest', file=f).draw_tree()
    assert re.match(u'└─ sha256:[a-f0-9]{5} footest:latest\n', f.getvalue())


def test_two_images():
    sh.docker(sh.cat('empty.tar'), 'import', '-', 'footest')
    sh.docker('build', '-t', 'bartest', '.')
    f = StringIO()
    Docktree(restrict='footest', file=f).draw_tree()
    assert re.match(
        u'└─ sha256:[a-f0-9]{5} footest:latest\n' +
        u'   └─ sha256:[a-f0-9]{5} bartest:latest\n', f.getvalue())
