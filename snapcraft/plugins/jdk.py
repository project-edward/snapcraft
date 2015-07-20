# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2015 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import snapcraft
from snapcraft.plugins.ubuntu import UbuntuPlugin


class JdkPlugin(snapcraft.BasePlugin):

    def __init__(self, name, options):
        super().__init__(name, options)

        class UbuntuOptions:
            package = "default-jdk"
        self.ubuntu = UbuntuPlugin(name, UbuntuOptions())

    def pull(self):
        return self.ubuntu.pull()

    def build(self):
        return self.ubuntu.build()

    def env(self, root):
        return self.ubuntu.env(root) + \
               ['JAVA_HOME=%s/usr/lib/jvm/default-java' % root,
                'PATH=%s/usr/lib/jvm/default-java/bin:%s/usr/lib/jvm/default-java/jre/bin:$PATH' % (root, root)]

    def snap_files(self):
        # Cut out jdk bits (jre bits are in default-java/jre)
        return (['*'], ['usr/lib/jvm/default-java/bin',
                        'usr/lib/jvm/default-java/include',
                        'usr/lib/jvm/default-java/lib'])
