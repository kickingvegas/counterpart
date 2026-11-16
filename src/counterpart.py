##
# Copyright 2026 Charles Y. Choi
#
# Open Texinfo URL in Emacs Info

# Given the URL of a web page generated from Texinfo, this code tries open its
# counterpart in GNU Emacs Info using Scrim on macOS.

# This code will only work on Texinfo HTML generated with one page per node.

# http://yummymelon.com/scrim/

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

import os
import sys
from subprocess import call
import re
from urllib.parse import quote, unquote, urlencode

VERSION = "0.0.1-rc.2"

use_scrim = True

# Set to your local configuration if use_scrim = False
emacsclient_path = "/Applications/MacPorts/Emacs.app/Contents/MacOS/bin/"

def cc_texinfo_urlpath_to_info(urlpath):
    "Convert urlpath to a Info node reference."

    if urlpath.find("/software/texinfo") >= 0:
        manual = "texinfo"
    elif urlpath.find("/software/coreutils") >= 0:
        manual = "coreutils"
    elif urlpath.find("/software/bash") >= 0:
        manual = "bash"
    else:
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

def cc_scrim_info_url(node):
    "Wrap node into a Scrim info URL."
    params = { "node" : node }
    info_node = urlencode(params, quote_via=quote)
    url = "scrim://info?{0}".format(info_node)
    return url

def cc_open_info_via_emacsclient(urlpath):
    "Open urlpath in emacsclient."
    emacsclient_exec = os.path.join(
        emacsclient_path,
        "emacsclient")
    node = cc_texinfo_urlpath_to_info(urlpath)
    url = "(info \"{0}\")".format(node)
    sys.stdout.write("{0}\n".format(url))
    call([emacsclient_exec, "-e", url])

def cc_open_info_via_scrim(urlpath):
    "Open urlpath in scrim."
    node = cc_texinfo_urlpath_to_info(urlpath)
    url = cc_scrim_info_url(node)
    sys.stdout.write("{0}\n".format(url))
    call(["open", url])

if __name__ == "__main__":
    urlpath = sys.argv[1]

    if use_scrim:
        cc_open_info_via_scrim(urlpath)
    else:
        cc_open_info_via_emacsclient(urlpath)
