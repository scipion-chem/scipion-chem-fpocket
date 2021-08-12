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

from ..protocols import FpocketFindPockets
import pyworkflow.protocol.params as params
import pyworkflow.viewer as pwviewer
from pwchem.viewers import PyMolViewer, PocketPointsViewer, ContactSurfaceViewer
from pwem.viewers import Vmd, VmdView

from subprocess import Popen


VOLUME_VMD, VOLUME_PYMOL, VOLUME_PYMOL_SURF = 0, 1, 2

class VmdViewFpocket(VmdView):
  def __init__(self, vmdArgs, **kwargs):
    pwviewer.CommandView.__init__(self, ['vmd', *vmdArgs.split()],
                                  env=Vmd.getEnviron(), **kwargs)

  def show(self):
    Popen(self._cmd, cwd=self._cwd, env=Vmd.getEnviron())

class viewerFPocket(pwviewer.ProtocolViewer):
  _label = 'Viewer pockets'
  _targets = [FpocketFindPockets]

  def __init__(self, **kwargs):
    pwviewer.ProtocolViewer.__init__(self, **kwargs)

  def _defineParams(self, form):
    form.addSection(label='Visualization of predicted pockets')
    form.addParam('displayAtomStruct', params.EnumParam,
                  choices=['VMD', 'PyMol (Pocket Points)', 'PyMol (Contact Surface)'],
                  default=VOLUME_VMD,
                  display=params.EnumParam.DISPLAY_HLIST,
                  label='Display output AtomStruct with',
                  help='*PyMol*: display AtomStruct and pockets as points / surface.\n '
                       '*VMD*: display AtomStruct and movies with VMD.'
                  )

  def _getVisualizeDict(self):
    return {
      'displayAtomStruct': self._showAtomStruct,
    }

  def _validate(self):
    return []

  # =========================================================================
  # ShowAtomStructs
  # =========================================================================

  def getOutputAtomStructFile(self):
    return os.path.abspath(self.protocol.outputAtomStruct.getFileName())

  def _showAtomStruct(self, paramName=None):
    if self.displayAtomStruct == VOLUME_PYMOL:
      return self._showAtomStructPyMol()

    elif self.displayAtomStruct == VOLUME_PYMOL_SURF:
      return self._showAtomStructPyMolSurf()

    elif self.displayAtomStruct == VOLUME_VMD:
      return self._showAtomStructVMD()

  def _showAtomStructPyMol(self):
    pymolV = PocketPointsViewer(project=self.getProject())
    pymolV._visualize(self.protocol.outputPockets)

  def _showAtomStructPyMolSurf(self):
    pymolV = ContactSurfaceViewer(project=self.getProject())
    pymolV._visualize(self.protocol.outputPockets)

  def _showAtomStructVMD(self):
    outFile = self.getOutputAtomStructFile().split('/')[-1]
    pdbName, _ = os.path.splitext(outFile)
    outDir = os.path.abspath(self.protocol._getExtraPath(pdbName))
    cmd = '{} -e {}'.format(outFile, pdbName.replace('_out', '.tcl'))

    viewer = VmdViewFpocket(cmd, cwd=outDir).show()