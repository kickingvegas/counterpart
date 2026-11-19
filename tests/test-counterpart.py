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

import unittest
from counterpart import *
from urllib.parse import urlsplit

class TestRegression(unittest.TestCase):

    def setUp(self):
        self.url_data = [
            "https://www.gnu.org/software/gettext/manual/html_node/Files.html"
            "https://www.gnu.org/software/emacs/manual/html_node/ccmode/index.html",
            "https://www.gnu.org/software/texinfo/manual/texinfo/html_node/index.html",
            "https://www.gnu.org/software/texinfo/manual/texinfo/html_node/Introducing-Lists.html",
            "https://kickingvegas.github.io/anju/Mode-Line-Features.html",
            "https://docs.magit.vc/magit/References-Buffer.html",
            "https://www.gnu.org/software/coreutils/manual/html_node/ls-invocation.html",
            "https://www.gnu.org/software/bash/manual/html_node/index.html",
            "https://www.gnu.org/software/make/manual/html_node/MAKEFILES-Variable.html"
        ]

        # TODO: maybe support orgmode.org website
        # https://orgmode.org/manual/Motion.html
        # https://orgmode.org/guide/Sparse-Trees.html

        self.paths = [urlsplit(x).path for x in self.url_data]
        #print(self.paths)

        self.data = (
            ('/software/gettext/manual/html_node/Files.html',
             'scrim://info?node=%28gettext%29%20Files'),
            ('/software/emacs/manual/html_node/ccmode/index.html',
             'scrim://info?node=%28ccmode%29%20Top'),
            ('/software/texinfo/manual/texinfo/html_node/index.html',
             'scrim://info?node=%28texinfo%29%20Top'),
            ('/software/texinfo/manual/texinfo/html_node/Introducing-Lists.html',
             'scrim://info?node=%28texinfo%29%20Introducing%20Lists'),
            ('/anju/Mode-Line-Features.html',
             'scrim://info?node=%28anju%29%20Mode%20Line%20Features'),
            ('/magit/References-Buffer.html',
             'scrim://info?node=%28magit%29%20References%20Buffer'),
            ('/software/coreutils/manual/html_node/ls-invocation.html',
             'scrim://info?node=%28coreutils%29%20ls%20invocation'),
            ('/software/bash/manual/html_node/index.html',
             'scrim://info?node=%28bash%29%20Top'),
            ('/software/make/manual/html_node/MAKEFILES-Variable.html',
             'scrim://info?node=%28make%29%20MAKEFILES%20Variable'),
        )


    def test_scrim_urls(self):
        "Test Scrim Info URLs with data."
        for urlpath, control in self.data:
            node = cpt_texinfo_urlpath_to_info(urlpath)
            result = cpt_scrim_info_url(node)
            self.assertEqual(result, control)


    def test_one_shot(self):
        "One shot test."
        urlpath = '/software/emacs/manual/html_node/ccmode/index.html'
        node = cpt_texinfo_urlpath_to_info(urlpath)
        result = cpt_scrim_info_url(node)
        control = 'scrim://info?node=%28ccmode%29%20Top'

        self.assertEqual(control, result)

if __name__ == '__main__':
    unittest.main()
