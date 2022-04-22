# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors: Daniel Del Hoyo (ddelhoyo@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
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
# *  e-mail address 'you@yourinstitution.email'
# *
# **************************************************************************


"""
This protocol is used to perform a pocket search on a protein structure using the FPocket software

"""

import os, shutil
import glob

from pyworkflow.protocol import params
from pyworkflow.utils import Message
from pyworkflow.object import String
from pwem.protocols import EMProtocol

from pwchem.objects import SetOfPockets, PredictPocketsOutput, ProteinPocket
from pwchem.utils import clean_PDB

from fpocket import Plugin
from fpocket.constants import *

class MDpocketCharacterize(EMProtocol):
    """
    Executes the mdpocket software to look for protein pockets.
    """
    _label = 'Characterization of pockets'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        """ """
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputSystem', params.PointerParam,
                       pointerClass='GromacsSystem', allowsNull=False,
                       label="Input atomic system: ",
                       help='Select the atom structure to search for pockets')

        form.addParam('selectedPocket', params.PointerParam,
                      pointerClass='SetOfPockets', allowsNull=False,
                      label="Set of pockets obtained from trajectory ",
                      help='Characterization of pockets obtained in MD trajectory')

    def _getMDpocketArgs(self, selPocket):
        trajFile = self.inputSystem.get().getTrajectoryFile()
        trajBasename = os.path.basename(trajFile)
        args = ['--trajectory_file', trajBasename]

        trajExt = os.path.splitext(trajFile)[1][1:]
        args += ['--trajectory_format', trajExt]

        pdbFile = self.inputSystem.get().getSystemFile()
        pdbBasename = os.path.basename(pdbFile)
        args += ['-f', pdbBasename]

        # selPocket = os.path.abspath(self.selectedPocket.get()._getExtraPath("pocketFile_1.pdb")
        args += ['--selected_pocket', selPocket]

        return args

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        # Insert processing steps
        self._insertFunctionStep('mdPocketStep')
        self._insertFunctionStep('createOutputStep')

    def mdPocketStep(self):

        for selPocket in (self.selectedPocket.get()):
            trajFile = os.path.abspath(self.inputSystem.get().getTrajectoryFile())
            pdbFile = os.path.abspath(self.inputSystem.get().getSystemFile())
            pocketFile = selPocket.getFileName()
            dir = os.path.abspath(self._getExtraPath('pocketFolder_{}'.format(selPocket.getObjId())))
            os.mkdir(dir)
            os.system('cd {} && cp {} {} {} ./'.format(dir, trajFile, pdbFile, os.path.abspath(pocketFile)))
            Plugin.runMDpocket_2(self, 'mdpocket', args=self._getMDpocketArgs(os.path.basename(pocketFile)), cwd=dir)
            os.system('rm {} {} {} ./'.format(trajFile, pdbFile, os.path.abspath(pocketFile)))

    def createOutputStep(self):
        pass



    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        summary = []
        return summary

    def _methods(self):
        methods = []
        return methods

    def _warnings(self):
        """ Try to find warnings on define params. """
        warnings = []
        return warnings

    # --------------------------- UTILS functions -----------------------------------
