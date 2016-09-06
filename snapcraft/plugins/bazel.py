# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2015, 2016 Canonical Ltd
# Copyright (C) 2016 Samuel Rosenstein <samr37l@gmail.com>
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

"""The bazel plugin is used for building with bazel.

This assumes that there is a WORKSPACE file at the root of the source directory with a corresponding BUILD file.

The plugin runs `bazel build <command> <flags>` 

This plugin uses the common plugin keywords as well as those for "sources".
For more information check the 'plugins' topic for the former and the
'sources' topic for the latter.

In addition, this plugin uses the following plugin-specific keywords:
    - command:
      (string)
      The build command for bazel to run
    - configflags:
      (list of strings)
      configure flags to pass to the build
"""

import os
import stat

import snapcraft


class AutotoolsPlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()

        schema['properties']['command'] = {
            'type': 'string',
            'default': "",
        }
        schema['properties']['configflags'] = {
            'type': 'array',
            'minitems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'default': [],
        }

        # Inform Snapcraft of the properties associated with building. If these
        # change in the YAML Snapcraft will consider the build step dirty.
        schema['build-properties'].extend(['command', 'configflags'])

        return schema

    def __init__(self, name, options, project):
        super().__init__(name, options, project)
        self.build_packages.extend([
            'bazel'
        ])

    def build(self):
        super().build()
        build_command = "bazel build {}".format(self.options.command)
        self.run(build_command + self.options.configflags) 

    def snap_fileset(self):
        fileset = super().snap_fileset()
        # Remove .la files which don't work when they are moved around
        fileset.append('-**/*.la')
        return fileset