# **************************************************************************
# *
# * Authors:     Daniel Del Hoyo (ddelhoyo@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
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

import pyworkflow.utils as pwutils
import pyworkflow.viewer as pwviewer

from modellerScipion.protocols import modellerMutateResidue


class PyMol:
    """ Help class to run PyMol and manage its environment. """

    @classmethod
    def getEnviron(cls):
        """ Return the proper environ to launch PyMol.
        PyMol_HOME variable is read from the ~/.config/scipion.conf file.
        """
        environ = pwutils.Environ(os.environ)
        environ.set('PATH', os.path.join(os.environ['PYMOL_HOME'], 'bin'),
                    position=pwutils.Environ.BEGIN)
        return environ


class PyMolView(pwviewer.CommandView):
    """ View for calling an external command. """
    def __init__(self, pymolCommand, cwd, **kwargs):
        pwviewer.CommandView.__init__(self, 'pymol %s' % pymolCommand,
                                      cwd=cwd,
                                      env=PyMol.getEnviron(), **kwargs)

    def show(self):
        pwutils.runJob(None, '', self._cmd, cwd=self._cwd, env=PyMol.getEnviron())


class PyMolViewer(pwviewer.Viewer):
    """ Wrapper to visualize pml objects with PyMol viewer. """
    _environments = [pwviewer.DESKTOP_TKINTER]
    _targets = [modellerMutateResidue]

    def __init__(self, **args):
        pwviewer.Viewer.__init__(self, **args)

    def visualize(self, pymolFile, cwd, **args):
        PyMolView(pymolFile, cwd).show()
