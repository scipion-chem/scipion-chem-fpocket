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

from ..protocols import MDpocketCharacterize
import pyworkflow.protocol.params as params
from pwchem.viewers import ViewerGeneralPockets
from pwchem.viewers import VmdViewPopen

class viewerMDPocket(ViewerGeneralPockets):
  _label = 'Viewer dynamic pockets MDPocket'
  _targets = [MDpocketCharacterize]

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def _defineParams(self, form):
    super()._defineParams(form)
    form.addSection(label='Pymol visualization')
    form.addParam('displayPymol', params.LabelParam,
                  label='Display output Pockets with Pymol: ',
                  help='*Pymol*: display dynamic Pockets along the MD simulation.')

  def _getVisualizeDict(self):
    dispDic = super()._getVisualizeDict()
    dispDic.update({'displayVMD': self._showAtomStructVMD})
    return dispDic

  def _validate(self):
    return []

  # =========================================================================
  # ShowAtomStructs
  # =========================================================================

  def _showAtomStructVMD(self, paramName=None):
    oPockets = self.protocol.outputPockets
    tclFile = oPockets.createTCL()
    outFile = oPockets.getProteinFile().split('/')[-1]
    pdbName, _ = os.path.splitext(outFile)
    outDir = os.path.abspath(self.protocol._getExtraPath(pdbName + '_out'))
    cmd = '{} -e {}'.format(outFile, tclFile)

    return [VmdViewPopen(cmd, cwd=outDir)]

