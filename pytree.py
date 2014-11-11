#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PyTree

Usage:
    pytree.py [options]
    pytree.py [options] <targetDir>

Options:
    -a, --all                  do not ignore entries starting with .
    -n                         colorization off
    -F, --classify             append indicator (one of */=>@|) to entries

Othres:
        --help      display this help and exit
        --version   output version information and exit

"""
from docopt import docopt
import os

C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_MAGENTA = '\033[95m'
C_CYAN = '\033[96m'
C_WHITE = '\033[97m'
C_END = '\033[00m'
C_BOLD = '\033[01m'


def listAlmostAllItems(path):
    items = os.listdir(path)
    sortKey = lambda f: f.lower() if not f.startswith('.') else f[1:].lower()
    items.sort(key=sortKey)
    return items


def listItems(path):
    items = listAlmostAllItems(path)
    return filter(lambda item: not item.startswith('.'), items)


def appendColor(path, item, color=False, classify=False):
    filepath = os.path.join(path, item)
    colorCode = ''
    endCode = C_END if color else ''
    indicator = ''
    if color:
        if os.path.islink(filepath):
            if os.path.isdir(filepath) or os.path.isfile(filepath):
                colorCode = C_CYAN
            else:
                colorCode = C_RED
        elif os.path.isdir(filepath):
            colorCode = C_BLUE
        elif os.access(filepath, os.X_OK):
            colorCode = C_GREEN
        else:
            colorCode = C_END

    if classify:
        if os.path.islink(filepath):
            indicator = '@'
        elif os.path.isdir(filepath):
            indicator = '/'
        elif os.access(filepath, os.X_OK):
            indicator = '*'

    return colorCode + item + endCode + indicator


def displayItem(path, item, color, classify):
    fullpath = os.path.join(path, item)
    string = appendColor(path, item, color, classify)
    if os.path.islink(fullpath):
        string += ' -> ' + appendColor(
            path,
            os.readlink(fullpath),
            color,
            classify)
    return string


def displayItems(path, prefix, color, classify, all):
    if all:
        items = listAlmostAllItems(path)
    else:
        items = listItems(path)
    for index, item in enumerate(items):
        fullpath = path + '/' + item
        if index == len(items)-1:
            print prefix + '└── ' + displayItem(path, item, color, classify)
            nextPrefix = prefix + '    '
        else:
            print prefix + '├── ' + displayItem(path, item, color, classify)
            nextPrefix = prefix + '│   '
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            displayItems(fullpath, nextPrefix, color, classify, all)

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0.0')

    # get directiory path ---------------------------
    if args['<targetDir>'] is None:
        path = '.'
    elif args['<targetDir>'].endswith('/'):
        path = args['<targetDir>'][:-1]
    else:
        path = args['<targetDir>']

    # list up items ---------------------------------
    print appendColor('', path, not args['-n'], args['--classify'])
    displayItems(path, '', not args['-n'], args['--classify'], args['--all'])
