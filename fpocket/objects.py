# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:  Alberto Manuel Parra Pérez (amparraperez@gmail.com)
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


from pwchem.objects import ProteinPocket, ProteinAtom, ProteinResidue
from .constants import ATTRIBUTES_MAPPING as AM
import numpy as np


class FpocketPocket(ProteinPocket):
  """ Represent a pocket file from fpocket"""
  def __init__(self, filename=None, proteinFile=None, propFile=None, **kwargs):
    if filename != None:
      self.properties, self.pocketId = self.parseFile(propFile)
      kwargs.update(self.getKwargs(self.properties, AM))

    super().__init__(filename, proteinFile, propFile, **kwargs)
    if hasattr(self, 'pocketId'):
      self.setObjId(self.pocketId)

  def __str__(self):
    s = 'Fpocket pocket {}\nFile: {}'.format(self.getObjId(), self.getFileName())
    return s

  def parseFile(self, filename):
    props, atoms, residues = {}, [], []
    atomsIds, residuesIds = [], []
    ini, parse = 'HEADER Information', False
    with open(filename) as f:
      for line in f:
        if line.startswith(ini):
          parse=True
          pocketId = int(line.split()[-1].replace(':', ''))
        elif line.startswith('HEADER') and parse:
          name = line.split('-')[1].split(':')[0]
          val = line.split(':')[-1]
          props[name.strip()] = float(val.strip())

        elif line.startswith('ATOM') and parse:
          atoms.append(ProteinAtom(line))
          atomsIds.append(atoms[-1].atomId)
          newResidue = ProteinResidue(line)
          if not newResidue.residueId in residuesIds:
            residues.append(newResidue)
            residuesIds.append(newResidue.residueId)
    props['contactAtoms'] = self.encodeIds(atomsIds)
    props['contactResidues'] = self.encodeIds(residuesIds)
    props['class'] = 'FPocket'
    return props, pocketId

  def getSpheresRadius(self):
    radius = []
    with open(str(self.getFileName())) as f:
      for line in f:
        if line.startswith('ATOM'):
          radius.append(float(line.split()[-1]))
    return radius

  def getDiameter(self):
    return super().getDiameter(radius=np.array(self.getSpheresRadius()))

  def calculateMassCenter(self):
    '''Calculates the center of mass of a set of points: [(x,y,z), (x,y,z),...]
    A weight for each point can be specified'''
    return super().calculateMassCenter(weights=self.getSpheresRadius())

