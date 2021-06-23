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
This protocol is used to perform a residue mutation in a protein structure.
A energy optimization is performed over the mutated residue and its surroundings.

"""
from pyworkflow.protocol import params
from pwem.protocols import EMProtocol
from pyworkflow.utils import Message
import os, shutil
from fpocket import Plugin
from pwem.objects.data import AtomStruct

class fpocketFindPockets(EMProtocol):
    """
    Performs a residue substitution in a protein structure.
    https://salilab.org/modeller/wiki/Mutate%20model
    """
    _label = 'Find pockets'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        """ """
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputAtomStruct', params.PointerParam,
                       pointerClass='AtomStruct', allowsNull=False,
                       label="Input atom structure",
                       help='Select the atom structure to be fitted in the volume')

    def _getFpocketArgs(self):
      args = ['-f', os.path.abspath(self.inpFile)]
      return args

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        # Insert processing steps
        self._insertFunctionStep('convertInputStep')
        self._insertFunctionStep('fPocketStep')
        self._insertFunctionStep('createOutputStep')

    def convertInputStep(self):
      #Simply copying the input struct file into current extra file (fpocket will create output there automatically)
      inpFile = self.inputAtomStruct.get().getFileName()
      inpName = inpFile.split('/')[-1]
      self.inpBase, self.ext = os.path.splitext(inpName)
      if self.ext == '.ent':
        self.inpFile = self._getExtraPath(self.inpBase+'.pdb')
      else:
        self.inpFile = self._getExtraPath(inpName)
      shutil.copy(inpFile, self.inpFile)

    def fPocketStep(self):
        Plugin.runFpocket(self, 'fpocket', args=self._getFpocketArgs(), cwd=self._getExtraPath())

    def createOutputStep(self):
        outFile = AtomStruct(self._getExtraPath('{}/{}'.format(
          self.inpBase+'_out', self.inpBase+'_out'+self.ext)))
        self._defineOutputs(outputPDB=outFile)

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        summary = []
        return summary

    def _methods(self):
        methods = []
        return methods
