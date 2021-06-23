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

from ..protocols import fpocketFindPockets
import pyworkflow.protocol.params as params
from pwem.viewers import EmProtocolViewer
import pyworkflow.utils as pwutils
from .viewers import PyMolViewer


VOLUME_VMD, VOLUME_PYMOL = 0, 1
FITTED_PDB, MOVIE_PDB = 0, 1

class viewerFPocket(EmProtocolViewer):
  _label = 'Viewer pockets'
  _targets = [fpocketFindPockets]

  def _defineParams(self, form):
    form.addSection(label='Visualization of predicted pockets')
    form.addParam('displayPDB', params.EnumParam,
                  choices=['VMD', 'PyMol'],
                  default=VOLUME_VMD,
                  display=params.EnumParam.DISPLAY_HLIST,
                  label='Display output PDB with',
                  help='*PyMol*: display AtomStruct as cartoons with '
                       'PyMol.\n *VMD*: display AtomStruct and movies with VMD.'
                  )

  def _getVisualizeDict(self):
    return {
      'displayPDB': self._showPDB,
    }

  def _validate(self):
    return []

  # =========================================================================
  # ShowPDBs
  # =========================================================================

  def _getPDBName(self):
    pdbFile = self.protocol.inputAtomStruct.get().getFileName()
    inpBase, _ = os.path.splitext(pdbFile.split('/')[-1])
    return inpBase

  def _showPDB(self, paramName=None):
    if self.displayPDB == VOLUME_PYMOL:
      return self._showPDBPyMol()

    elif self.displayPDB == VOLUME_VMD:
      return self._showPDBVMD()

  def _showPDBPyMol(self):
    pdbName = self._getPDBName()
    outDir = os.path.abspath(self.protocol._getExtraPath(pdbName + '_out'))
    pymolFile = outDir + '/' + pdbName + '.pml'

    vmdV = PyMolViewer(project=self.getProject())
    vmdV.visualize(pymolFile, cwd=outDir)

  def _showPDBVMD(self):
    pdbName = self._getPDBName()
    outDir = os.path.abspath(self.protocol._getExtraPath(pdbName + '_out'))
    pwutils.runJob(None, outDir + '/' + pdbName + '_VMD.sh', '', cwd=outDir)

