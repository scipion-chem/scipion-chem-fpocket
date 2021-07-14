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


from pwchem.objects import proteinPocket


class fpocketPocket(proteinPocket):
  """ Represent a pocket file from fpocket"""
  def __init__(self, filename=None, **kwargs):
    proteinPocket.__init__(self, filename, **kwargs)
    self.properties, self.pocketId = self.parseFile(filename)
    self.setObjId(self.pocketId)

  def __str__(self):
    s = 'Fpocket pocket {}\nFile: {}'.format(self.pocketId, self.getFileName())
    return s

  def getVolume(self):
    return self.properties['Real volume (approximation)']

  def getPocketScore(self):
    return self.properties['Pocket Score']

  def getNumberOfVertices(self):
    return self.properties['Number of V. Vertices']

  def parseFile(self, filename):
    props = {}
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
    return props, pocketId
