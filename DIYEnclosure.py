# -*- coding: utf-8 -*-
###################################################################################
#
#  InitGui.py
#  
#  Copyright 2015 Shai Seger <shaise at gmail dot com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
###################################################################################
from PySide import QtGui, QtCore
import FreeCAD,FreeCADGui 
import CrazyHomeEnclosureData, CrazyHomeEnclosureGUI, CrazyHomeEnclosureGenerator
import os

aCurrDir = os.path.dirname(__file__)
iconsPath = os.path.join( aCurrDir, 'resources' )
generatoricon = os.path.join( iconsPath, 'generator.png' )
 
class DIYEnclosure:
  "DIY Enclosure object"
 
  def GetResources(self):
    return {"MenuText": "Create Enclosure",
            "Accel": "Ctrl+G",
            "ToolTip": "Create enclosure for electronic devices",
            "Pixmap"  : generatoricon}

  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False
    else:
      return True
 
  def Activated(self):
    aParameters = CrazyHomeEnclosureData.EnclosureParameters()
    aParameters.restoreFromSettings()
    aControlPanel = CrazyHomeEnclosureGUI.EnclosureControlPanel()
    aControlPanel.setParameters(aParameters)
    aRes = aControlPanel.exec_()
    aControlPanel.fillParameters(aParameters)
    aParameters.saveToSettings()
    if aRes == QtGui.QDialog.Accepted:
      if FreeCAD.activeDocument() is None:
        aDoc = FreeCAD.newDocument("Enclosure")
        FreeCAD.ActiveDocument=aDoc
        FreeCAD.Gui.ActiveDocument=aDoc
      aGenerator = CrazyHomeEnclosureGenerator.EnclosureGenerator(aParameters)
      aGenerator.generate()
      FreeCAD.Gui.SendMsgToActiveView("ViewFit")

FreeCADGui.addCommand('DIYEnclosure',DIYEnclosure())
               