# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import sys


# Source tarbal contains two versions: KDE (Kcachegrind) and QT (Qcachegrind)
class Qcachegrind(Package):
    """Profile data visualization tool for Callgrind."""

    homepage = "https://kcachegrind.github.io/"
    url = 'https://download.kde.org/stable/applications/18.04.3/src/kcachegrind-18.04.3.tar.xz'

    version ('18.04.3', '2370827f8d3c29ec931fc3ebf34726e42d25aaaab6c2f10dc5dd87f57056acfd')

    depends_on('qt@4.5:')
    depends_on('graphviz', type='run')

#    parallel = False

    def install(self, spec, prefix):
        args = [
            '-config',
            'release'
        ]

        if (sys.platform == 'darwin') and spec.satisfies('%clang'):
            args.extend([
                '-spec',
                'macx-clang'
            ])

        Executable('qmake')(*args)
        make()

        bin_location = self.prefix.bin
        mkdirp(bin_location)
        bins = glob.glob(join_path(self.stage.source_path, 'bin', '*'))
        for b in bins:
            install(b, bin_location)

        if (sys.platform == 'darwin'):
            install('qcachegrind.app', prefix)
            # https://github.com/Homebrew/homebrew-core/blob/master/Formula/qcachegrind.rb
            # bin.install_symlink prefix/"qcachegrind.app/Contents/MacOS/qcachegrind"
