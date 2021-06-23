# **************************************************************************
# *
# * Authors:  Daniel Del Hoyo (ddelhoyo@cnb.csic.es)
# *
# * Biocomputing Unit, CNB-CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import pwem
from os.path import join, exists
from .constants import *

_version_ = '0.1'
_logo = "fpocket_logo.png"
_references = ['']


class Plugin(pwem.Plugin):
    _homeVar = FPOCKET_HOME
    _pathVars = [FPOCKET_HOME]
    _supportedVersions = [V3_0]
    _pluginHome = join(pwem.Config.EM_ROOT, FPOCKET + '-' + FPOCKET_DEFAULT_VERSION)

    @classmethod
    def _defineVariables(cls):
        """ Return and write a variable in the config file.
        """
        cls._defineEmVar(FPOCKET_HOME, FPOCKET + '-' + FPOCKET_DEFAULT_VERSION)

    @classmethod
    def defineBinaries(cls, env):
        installationCmd = ''
        print('Installing with conda')
        installationCmd += 'conda install -c conda-forge fpocket -p {} && '.format(cls._pluginHome)

        # Creating validation file
        MODELLER_INSTALLED = '%s_installed' % FPOCKET
        installationCmd += 'touch %s' % MODELLER_INSTALLED  # Flag installation finished

        env.addPackage(FPOCKET,
                       version=FPOCKET_DEFAULT_VERSION,
                       tar='void.tgz',
                       commands=[(installationCmd, MODELLER_INSTALLED)],
                       neededProgs=["conda"],
                       default=True)

    @classmethod
    def runFpocket(cls, protocol, program, args, cwd=None):
        """ Run Modeller command from a given protocol. """
        print(protocol)
        protocol.runJob(join(cls._pluginHome, 'bin/{}'.format(program)), args, cwd=cwd)

    @classmethod  #  Test that
    def getEnviron(cls):
        pass

    # ---------------------------------- Utils functions  -----------------------

