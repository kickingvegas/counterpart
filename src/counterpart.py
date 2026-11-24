#!/usr/bin/env python3

## counterpart.py --- Open Texinfo URL in Emacs Info

# Copyright (C) 2026 Charles Y. Choi

# Author: Charles Choi <kickingvegas@gmail.com>
# Keywords: tools

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Commentary

# Counterpart is a macOS utility to open the counterpart of a Texinfo web page
# in GNU Emacs Info.

# Counterpart requires usage of the Safari web browser and installation of an
# iCloud Shortcut.

# Counterpart only works on Texinfo HTML generated with one page per node.

## Code

import os
import sys
from subprocess import call
import re
from urllib.parse import quote, unquote, urlencode, urlsplit
import argparse

VERSION = "0.2.1-rc.1"

use_scrim = True

# Set to your local configuration if use_scrim = False
emacsclient_path = "/Applications/MacPorts/Emacs.app/Contents/MacOS/bin/"


def is_gnu_manual(urlpath):
    "Predicate if urlpath is a GNU manual that is not Emacs."
    pat = re.compile(r"^/software/(\w*)/")

    match = pat.search(urlpath)

    if match:
        result = match.group(1)
    else:
        result = None

    return result

def cpt_texinfo_urlpath_to_info(urlpath):
    "Convert urlpath to a Info node reference."

    manual = is_gnu_manual(urlpath)

    if (not manual) or (manual == "emacs"):
        manual = os.path.basename(os.path.dirname(urlpath))

    if os.path.splitext(urlpath)[1] == '':
        filename = ''
    else:
        _, filename = os.path.split(urlpath)

    if filename not in ("index.html", ''):
        filename, _ = os.path.splitext(filename)
        filename = filename.replace("-" , " ")
        # This makes the strong presumption the following regex works.
        pat = r"_00([0-9a-f][0-9a-f])"
        filename = re.sub(pat, lambda m: unquote(f"%{m.group(1)}"), filename)
        node = "({0}) {1}".format(manual, filename)

    else:
        node = "({0}) Top".format(manual)

    return node

def cpt_scrim_info_url(node):
    "Wrap node into a Scrim info URL."
    params = { "node" : node }
    info_node = urlencode(params, quote_via=quote)
    url = "scrim://info?{0}".format(info_node)
    return url

def cpt_open_info_via_emacsclient(urlpath):
    "Open urlpath in emacsclient."
    emacsclient_exec = os.path.join(
        emacsclient_path,
        "emacsclient")
    node = cpt_texinfo_urlpath_to_info(urlpath)
    url = "(info \"{0}\")".format(node)
    sys.stdout.write("{0}\n".format(url))
    call([emacsclient_exec, "-e", url])

def cpt_open_info_via_scrim(urlpath):
    "Open urlpath in scrim."
    node = cpt_texinfo_urlpath_to_info(urlpath)
    url = cpt_scrim_info_url(node)
    sys.stdout.write("{0}\n".format(url))
    call(["open", url])


def cpt_parse_args(args):
    "Parse command line arguments args."
    parser = argparse.ArgumentParser(
                    prog='counterpart',
                    description='Convert Texinfo web page reference to Info node.',
                    epilog='')

    parser.add_argument('reference',
                        help='Either URL path or URL.')

    parser.add_argument('-v', '--version',
                        action='version',
                        version=VERSION,
                        help='print version information and exit')

    parser.add_argument('-s', '--shortcut',
                        action=argparse.BooleanOptionalAction,
                        default=True,
                        help='If set, run as if invoked via macOS Shortcut.')

    parser.add_argument('-e', '--execute',
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help=('Open counterpart reference. '
                              'Only valid when --no-shortcut is used.'))

    parser.add_argument('-p', '--path',
                        type=str,
                        default=emacsclient_path,
                        help=('Path to emacsclient. '
                              'Only valid when --no-shortcut is used.'))

    parser.add_argument('-t', '--target',
                        choices=['scrim', 'info'],
                        default='info',
                        help=('Target format. '
                              'Only valid when --no-shortcut is used.'))

    return parser.parse_args(args)


if __name__ == "__main__":
    args = cpt_parse_args(sys.argv[1:])

    if args.reference.find("http") == 0:
        url = urlsplit(args.reference)
        urlpath = url.path
    else:
        urlpath = args.reference

    if args.shortcut:
        if use_scrim:
            cpt_open_info_via_scrim(urlpath)
        else:
            cpt_open_info_via_emacsclient(urlpath)

    else:
        node = cpt_texinfo_urlpath_to_info(urlpath)
        if args.target == 'scrim':
            url = cpt_scrim_info_url(node)
            if args.execute:
                call(["open", url])

        elif args.target == 'info':
            url = "(info \"{0}\")".format(node)
            if args.execute:
                emacsclient_exec = os.path.join(
                    args.path,
                    "emacsclient")
                call([emacsclient_exec, "-e", url])

        sys.stdout.write("{0}\n".format(url))
