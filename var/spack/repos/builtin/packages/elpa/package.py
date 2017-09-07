##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Elpa(AutotoolsPackage):
    """Eigenvalue solvers for Petaflop-Applications (ELPA)"""

    homepage = 'http://elpa.mpcdf.mpg.de/'
    url = 'http://elpa.mpcdf.mpg.de/elpa-2015.11.001.tar.gz'

    version('2017.05.002', 'd0abc1ac1f493f93bf5e30ec8ab155dc')
    version('2016.11.001.pre', '5656fd066cf0dcd071dbcaf20a639b37')
    version('2016.05.004', 'c0dd3a53055536fc3a2a221e78d8b376')
    version('2016.05.003', '88a9f3f3bfb63e16509dd1be089dcf2c')
    version('2015.11.001', 'de0f35b7ee7c971fd0dca35c900b87e6')

    version('develop', git='https://gitlab.mpcdf.mpg.de/elpa/elpa.git')

    variant('openmp', default=False, description='Activates OpenMP support')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')

    depends_on('gmake@4.2.1:', when='platform=darwin')
    depends_on('gawk', when='platform=darwin')
    depends_on("autoconf", type='build')
    depends_on("automake", type='build')
    depends_on("libtool", type='build')
    depends_on("perl", type='build')

    def url_for_version(self, version):
        t = 'http://elpa.mpcdf.mpg.de/html/Releases/{0}/elpa-{0}.tar.gz'
        if version < Version('2016.05.003'):
            t = 'http://elpa.mpcdf.mpg.de/elpa-{0}.tar.gz'
        return t.format(str(version))

    # override default implementation which returns static lib
    @property
    def libs(self):

        libname = 'libelpa_openmp' if '+openmp' in self.spec else 'libelpa'

        return find_libraries(
            libname, root=self.prefix, shared=True, recurse=True
        )

    build_directory = 'spack-build'
    # parallel = False

    # def setup_environment(self, spack_env, run_env):
    #    spack_env.set('SCALAPACK_LDFLAGS', math_libs.ld_flags())

    def configure_args(self):
        # TODO: set optimum flags for platform+compiler combo, see
        # https://github.com/hfp/xconfigure/tree/master/elpa
        spec = self.spec
        math_libs = spec['scalapack'].libs + spec['lapack'].libs + \
            spec['blas'].libs

        options = [
            'CC=%s' % spec['mpi'].mpicc,
            'FC=%s' % spec['mpi'].mpifc,
            'CXX=%s' % spec['mpi'].mpicxx,
            '--with-mpi=yes',
            'FCFLAGS=-O3 -march=native',
            'CFLAGS=-O3 -march=native',
            'SCALAPACK_LDFLAGS=%s' % math_libs.ld_flags
        ]

        if spec.satisfies('platform=darwin'):
            options.extend([
                '--disable-sse-assembly',
                '--disable-avx',
                '--disable-avx2'
            ])
        if '+openmp' in spec:
            options.append("--enable-openmp")
        return options
