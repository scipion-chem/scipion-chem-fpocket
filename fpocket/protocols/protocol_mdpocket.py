# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors: Daniel Del Hoyo (ddelhoyo@cnb.csic.es)
# *          Lobna Ramadane Morchadi (lobna.ramadane@alumnos.upm.es)
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

from pyworkflow.protocol import params
from pyworkflow.utils import Message
from pyworkflow.object import String
from pwem.protocols import EMProtocol

from pwchem.objects import SetOfPockets, PredictPocketsOutput, ProteinPocket
from pwchem.utils import clean_PDB

from fpocket import Plugin
from fpocket.constants import *

class MDpocketAnalyze(EMProtocol):
    """
    Executes the mdpocket software to look for protein pockets.
    """
    _label = 'Analyze pockets'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        """ """
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputSystem', params.PointerParam,
                       pointerClass='GromacsSystem', allowsNull=False,
                       label="Input atomic system: ",
                       help='Select the atom structure to search for pockets')

        form.addSection(label='Pocket analysis parameters')
        group = form.addGroup('Features')
        group.addParam('doGenerateReferences', params.BooleanParam, default=False,
                       label='Druggable Pockets',
                       help='If *No*, default parameters to select all pockets \t'
                            'If *Yes*, to score pockets by druggability'
                            'Identification of pockets most likely to bind drug like molecules'
                       )

        group.addParam('isoValue', params.FloatParam, default=1.0,
                       label='Selected Isovalue',
                       help='Selected Isovalue Threshold in Pocket Analysis for PDB output')

    def _getMDpocketArgs(self):
        trajFile = os.path.abspath(self.inputSystem.get().getTrajectoryFile())
        args = ['--trajectory_file', trajFile]

        trajExt = os.path.splitext(trajFile)[1][1:]
        args += ['--trajectory_format', trajExt]

        pdbFile = os.path.abspath(self.inputSystem.get().getSystemFile())
        args += ['-f', pdbFile]

        selPock = self.doGenerateReferences.get()
        if selPock == True:
            args += ['-S']

        args +=['-C']

        return args

    def _getselIsovalueArgs(self):
    # python extractISOPdb.py path / my_dx_file.dx outputname.pdb isovalue

        volFile = os.path.abspath(self._getExtraPath("mdpout_dens_grid.dx")) #To get the extra path between home path and protocol
        args = [volFile]

        outputName = 'mdpoutput-{}.pdb'.format(str(self.isoValue.get()))
        args += [outputName]

        isoValue = self.isoValue.get()
        args += [isoValue]

        return args
    #
    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        # Insert processing steps
        self._insertFunctionStep('mdPocketStep')
        self._insertFunctionStep('createOutputStep')
        self._insertFunctionStep('selIsovalue')
    def mdPocketStep(self):
        Plugin.runMDpocket(self, 'mdpocket', args=self._getMDpocketArgs(), cwd=self._getExtraPath())

    def selIsovalue(self):
        Plugin.runSelIsovalue(self, 'extractISOPdb.py', args=self._getselIsovalueArgs(), cwd=self._getExtraPath())

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
