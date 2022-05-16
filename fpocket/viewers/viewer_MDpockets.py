# **************************************************************************
# *
# * Authors:     Lobna Ramadane Morchadi (lobna.ramadane@alumnos.upm.es)
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
import os, glob

import matplotlib.pyplot as plt
import numpy as np
import pyworkflow.viewer as pwviewer

from ..protocols import MDpocketCharacterize
import pyworkflow.protocol.params as params
from pwchem.viewers import  PyMolView
from pwchem.utils import natural_sort

from pwem.viewers.plotter import EmPlotter, plt


class viewerMDPocket(pwviewer.ProtocolViewer):
  _label = 'Viewer dynamic pockets of MDPocket'
  _targets = [MDpocketCharacterize]

  def __init__(self, **kwargs):
      pwviewer.ProtocolViewer.__init__(self, **kwargs)

  def _defineParams(self, form):
    form.addSection(label='Pymol visualization')
    form.addParam('displayPymol', params.LabelParam,
                  label='Display output Pockets with Pymol: ',
                  help='*Pymol*: display dynamic Pockets along the MD simulation.')


    group = form.addGroup('Pockets to view')
    group.addParam('nPocket', params.EnumParam, default=0, #enumParam para ver la lista de carpetas
                   choices= self._getDynPockets(),
                   label='Choose the pocket to visualize:',
                   help='Selected pockets and protein atom interactions to visualize along the MD trajectory')


    form.addSection(label='Graphic view')
    form.addParam('displayGraphic', params.LabelParam,
                  label='Display a graph of selected pocket: ',
                  help='Display a graphical representation of descriptors of selected pockets along MD trajectory')


  def _getVisualizeDict(self):
      return {
        'displayPymol': self._showMdPymol,
        'displayGraphic': self._displayGraphic
      }

  def _validate(self):
    return []

  # =========================================================================

  def _showMdPymol(self, paramName=None):
    PYMOL_MD_POCK = ''' load {}
    load_traj {}
    set movie_fps, 15
    load {}
    load {}
    
    '''
    pdbFile = self.protocol.inputSystem.get().getSystemFile()
    trjFile = self.protocol.inputSystem.get().getTrajectoryFile()
    dir = os.path.abspath(self.protocol._getExtraPath('pocketFolder_{}'.format(str(self.nPocket.get()))))
    dynPocket ='{}/mdpout_mdpocket_{}.pdb'.format(dir, str(self.nPocket.get()))
    dynAtoms = '{}/mdpout_mdpocket_atoms_{}.pdb'.format(dir, str(self.nPocket.get()))
    outPml = self.protocol._getExtraPath('pymolSimulation.pml')
    with open(outPml, 'w') as f:
      f.write(PYMOL_MD_POCK .format(os.path.abspath(pdbFile),
                                    os.path.abspath(trjFile),
                                    os.path.abspath(dynPocket),
                                    os.path.abspath(dynAtoms)))



    return [PyMolView(os.path.abspath(outPml), cwd=self.protocol._getPath())]


  def _getDynPockets(self):
      n_pockets = []
      for pockDir in natural_sort(glob.glob(self.protocol._getExtraPath('pocketFolder_*'))):
          n_pocket = os.path.basename(pockDir)
          n_pocket = n_pocket.split('_')[1]
          n_pockets.append(n_pocket)

      return n_pockets


  def _displayGraphic(self,  paramName=None):
      dir = os.path.abspath(self.protocol._getExtraPath('pocketFolder_{}'.format(str(self.nPocket.get()+1))))
      descrFile = '{}/mdpout_descriptors_{}.txt'.format(dir, str(self.nPocket.get()+1))
      fileTxt = open(descrFile, 'r')
      file = fileTxt.readlines()[1:]
      y =[]
      for descriptors in file:
          line = descriptors.split()
          desc = line[1:3]
          desc = list(map(float, desc))
          y.append(desc)


      snaps = []
      for descriptors in file:
          line = descriptors.split()
          desc = line[0]
          snaps.append(desc)


      #graphDesc = plt.plot(snaps, y)
      self.plotter = EmPlotter(x = 1, y = 1, windowTitle='Pocket Descriptors')
      a = self.plotter.createSubPlot("Pocket {} ".format(str(self.nPocket.get())), "Snapshots", "Descriptors")
      a.plot(snaps, y)
      return [self.plotter]


