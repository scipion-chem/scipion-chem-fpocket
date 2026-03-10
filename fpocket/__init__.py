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

import os
from os.path import join

from scipion.install.funcs import InstallHelper
from pwchem.constants import OPENBABEL_DIC

from pwchem import Plugin as pwchemPlugin
from .constants import *

_version_ = '0.1'
_logo = "fpocket_logo.png"
_references = ['']


class Plugin(pwchemPlugin):
    _homeVar = OPENBABEL_DIC['home']
    _pathVars = [OPENBABEL_DIC['home']]
    _supportedVersions = [OPENBABEL_DIC['version']]

    @classmethod
    def _defineVariables(cls):
        """ Return and write a variable in the config file.
        """
        cls._defineEmVar(OPENBABEL_DIC['home'], OPENBABEL_DIC['name'] + '-' + OPENBABEL_DIC['version'])

    @classmethod
    def defineBinaries(cls, env, default=True):
        installer = InstallHelper(OPENBABEL_DIC['name'], packageHome=cls.getVar(OPENBABEL_DIC['home']),
                                  packageVersion=OPENBABEL_DIC['version'])

        installer.addCondaPackages(
            ["fpocket"],  # install binary
            channel="conda-forge",
            targetName="fpocket_installed"
        )

        scriptsDir = ("scripts")
        installer.addCommand(f'mkdir -p "{scriptsDir}"', 'create_scripts_dir')

        githubBase = "https://raw.githubusercontent.com/Discngine/fpocket/master/scripts"
        script = "extractISOPdb.py"
        installer.addCommand(
            f'curl -L {githubBase}/{script} -o "{scriptsDir}/{script}"',
            f'download_{script}'
        )
        installer.addCommand(f'chmod +x "{scriptsDir}/{script}"')

        installer.addPackage(env, dependencies=['conda'], default=default)

    @classmethod
    def getPluginHome(cls, path=""):
        import fpocket
        fnDir = os.path.split(fpocket.__file__)[0]
        return os.path.join(fnDir, path)

    @classmethod
    def getScriptsDir(cls, scriptName):
        return cls.getPluginHome('scripts/%s' % scriptName)

    @classmethod
    def runFpocket(cls, protocol, program, args, cwd=None):
        """ Run Fpocket command from a given protocol. """
        protocol.runJob(os.path.join(cls.getVar(OPENBABEL_DIC['home']), 'bin/{}'.format(program)), args, cwd=cwd)

    @classmethod
    def runMDpocket(cls, protocol, program, args, cwd):
        """ Run MDpocket command from a given protocol. """
        protocol.runJob(f'./{program}', arguments=args, cwd=cwd)


