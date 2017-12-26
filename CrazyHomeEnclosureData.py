# -*- coding: utf-8 -*-

# Macro Begin: D:\3dPrinter\FreeCADMacroses\CrazyHomeEnclosure.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
import FreeCAD
import Part
from PySide import QtGui, QtCore

OrganizationName = "CrazyHome"
AppName = "EnclosureFreeCADPlugin"

def getSettingsBool(theSettings,theKey,theDefault):
  aStr = theSettings.value(theKey)
  if aStr is None:
    return theDefault
  if aStr == "true":
    return True
  return False

class GeneralParameters:
  SettSection = "General"

  def __init__(self):
# Box external length in mm
    self.m_Length = 115.
# Box external width in mm
    self.m_Width = 95.
# Box external height in mm
    self.m_TotalHeight = 24.
#Bottom part height without notch in mm
    self.m_BottomHeight = 12.
#Notch height in mm
    self.m_NotchHeight = 1.
#Bottom and Top borders width in mm
    self.m_HorizontalBorderWidth = 1.5
#Vertical borders width in mm
    self.m_VerticalBorderWidth = 3.

  def saveToSettings(self,theSett):
    theSett.beginGroup(self.SettSection)
    theSett.setValue("Length",self.m_Length)
    theSett.setValue("Width",self.m_Width)
    theSett.setValue("TotalHeight",self.m_TotalHeight)
    theSett.setValue("BottomHeight",self.m_BottomHeight)
    theSett.setValue("NotchHeight",self.m_NotchHeight)
    theSett.setValue("VerticalBorderWidth",self.m_VerticalBorderWidth)
    theSett.setValue("HorizontalBorderWidth",self.m_HorizontalBorderWidth)
    theSett.endGroup()

  def restoreFromSettings(self,theSett):
    theSett.beginGroup(self.SettSection)
    self.m_Length = float(theSett.value("Length",115.))
    self.m_Width = float(theSett.value("Width",95.))
    self.m_TotalHeight = float(theSett.value("TotalHeight",24.))
    self.m_BottomHeight = float(theSett.value("BottomHeight",12.))
    self.m_NotchHeight = float(theSett.value("NotchHeight",1.))
    self.m_VerticalBorderWidth = float(theSett.value("VerticalBorderWidth",3.))
    self.m_HorizontalBorderWidth = float(theSett.value("HorizontalBorderWidth",1.5))
    theSett.endGroup()
          
class HoleParameters:
  BOTTOM_DIRECTION=0
  TOP_DIRECTION=1

  def __init__(self):
    self.m_isCreate = True
    self.m_Direction = self.BOTTOM_DIRECTION
    self.m_Radius = 2.
    self.m_Height = 30.

  def saveToSettings(self,theSett,theGroup):
    theSett.beginGroup(theGroup)
    theSett.setValue("isCreate",self.m_isCreate)
    theSett.setValue("Direction",self.m_Direction)
    theSett.setValue("Radius",self.m_Radius)
    theSett.setValue("Height",self.m_Height)
    theSett.endGroup()

  def restoreFromSettings(self,theSett,theGroup):
    theSett.beginGroup(theGroup)
    self.m_isCreate = getSettingsBool(theSett,"isCreate",True)
    self.m_Direction = int(theSett.value("Direction",self.BOTTOM_DIRECTION))
    self.m_Radius = float(theSett.value("Radius",2.))
    self.m_Height = float(theSett.value("Height",30.))
    theSett.endGroup()

class CustomStandParameters:
  def __init__(self):
    self.m_StandRadius = 4.
    self.m_Height = 2.
    self.m_X = 30.
    self.m_Y = 30.
    self.m_Hole = HoleParameters()

  def saveToSettings(self,theSett,theGroup):
    theSett.beginGroup(theGroup)
    theSett.setValue("Radius",self.m_StandRadius)
    theSett.setValue("Height",self.m_Height)
    theSett.setValue("X",self.m_X)
    theSett.setValue("Y",self.m_Y)
    self.m_Hole.saveToSettings(theSett,"Hole")
    theSett.endGroup()

  def restoreFromSettings(self,theSett,theGroup):
    theSett.beginGroup(theGroup)
    self.m_StandRadius = float(theSett.value("Radius",4.0))
    self.m_Height = float(theSett.value("Height",2.))
    self.m_X = float(theSett.value("X",30.))
    self.m_Y = float(theSett.value("Y",30.))
    self.m_Hole.restoreFromSettings(theSett,"Hole")
    theSett.endGroup()

class EarParameters:
  BOTTOM_DIRECTION=0
  TOP_DIRECTION=1
  FRONT_DIRECTION=2
  BACK_DIRECTION=3
  LEFT_DIRECTION=4
  RIGHT_DIRECTION=5
  CUSTOM_OFFSET=6
  def __init__(self):
    self.m_Length = 12.
    self.m_Width = 12.
    self.m_Height = 3.
    self.m_Base = self.BOTTOM_DIRECTION
    self.m_Direction = self.LEFT_DIRECTION
    self.m_Align = self.FRONT_DIRECTION
    self.m_Offset = 0.
    self.m_HoleX = 6.
    self.m_HoleY = 6.
    self.m_isCenterHole = True
    self.m_Hole = HoleParameters()

  def saveToSettings(self,theSett,theGroup):
    theSett.beginGroup(theGroup)
    theSett.setValue("Length",self.m_Length)
    theSett.setValue("Width",self.m_Width)
    theSett.setValue("Height",self.m_Height)
    theSett.setValue("Base",self.m_Base)
    theSett.setValue("Direction",self.m_Direction)
    theSett.setValue("Align",self.m_Align)
    theSett.setValue("Offset",self.m_Offset)
    theSett.setValue("HoleX",self.m_HoleX)
    theSett.setValue("HoleY",self.m_HoleY)
    theSett.setValue("isCenterHole",self.m_isCenterHole)
    self.m_Hole.saveToSettings(theSett,"Hole")
    theSett.endGroup()

  def restoreFromSettings(self,theSett,theGroup):
    theSett.beginGroup(theGroup)
    self.m_Length = float(theSett.value("Length",12.))
    self.m_Width = float(theSett.value("Width",12.))
    self.m_Height = float(theSett.value("Height",3.))
    self.m_Base = int(theSett.value("Base",self.BOTTOM_DIRECTION))
    self.m_Direction = int(theSett.value("Direction",self.LEFT_DIRECTION))
    self.m_Align = int(theSett.value("Align",self.BACK_DIRECTION))
    self.m_Offset = float(theSett.value("Offset",0.))
    self.m_HoleX = float(theSett.value("HoleX",6.))
    self.m_HoleY = float(theSett.value("HoleY",6.))
    self.m_isCenterHole = getSettingsBool(theSett,"isCenterHole",True)
    self.m_Hole.restoreFromSettings(theSett,"Hole")
    theSett.endGroup()

class PanelParameters:
  def __init__(self):
    self.m_isCreate = True
    self.m_Length = 26.
    self.m_Height = 15.
    self.m_isCenterPanel = False
    self.m_Offset = 56.
    self.m_BorderHeight = 1.5
    self.m_isDefaultBorderWidth = True
    self.m_BorderWidth = 1.
    self.m_isCreateSimplePanel = True
    self.m_BorderWidthReduce = 0.2

  def saveToSettings(self,theSett,theGroup):
    theSett.beginGroup(theGroup)
    theSett.setValue("isCreate",self.m_isCreate)
    theSett.setValue("Length",self.m_Length)
    theSett.setValue("Height",self.m_Height)
    theSett.setValue("isCenterPanel",self.m_isCenterPanel)
    theSett.setValue("Offset",self.m_Offset)
    theSett.setValue("BorderHeight",self.m_BorderHeight)
    theSett.setValue("isDefaultBorderWidth",self.m_isDefaultBorderWidth)
    theSett.setValue("BorderWidth",self.m_BorderWidth)
    theSett.setValue("isCreateSimplePanel",self.m_isCreateSimplePanel)
    theSett.setValue("BorderWidthReduce",self.m_BorderWidthReduce)
    theSett.endGroup()

  def restoreFromSettings(self,theSett,theGroup):
    theSett.beginGroup(theGroup)
    self.m_isCreate = getSettingsBool(theSett,"isCreate",True)
    self.m_Length = float(theSett.value("Length",26.))
    self.m_Height = float(theSett.value("Height",15.))
    self.m_isCenterPanel = getSettingsBool(theSett,"isCenterPanel",True)
    self.m_Offset = float(theSett.value("Offset",56.))
    self.m_BorderHeight = float(theSett.value("BorderHeight",1.5))
    self.m_isDefaultBorderWidth = getSettingsBool(theSett,"isDefaultBorderWidth",True)
    self.m_BorderWidth = float(theSett.value("BorderWidth",1.))
    self.m_isCreateSimplePanel = getSettingsBool(theSett,"isCreateSimplePanel",True)
    self.m_BorderWidthReduce = float(theSett.value("BorderWidthReduce",0.2))
    theSett.endGroup()

class EnclosureStandParameters:
  SettSection = "EnclosureStands"
  def __init__(self):
#Radius of enclosure stand
    self.m_StandRadius = 4.
    self.m_StandOffset = -1.5
    self.m_TopLeftCreate = True
    self.m_TopRightCreate = True
    self.m_BottomLeftCreate = True
    self.m_BottomRightCreate = True
    self.m_BottomHole = HoleParameters()
    self.m_BottomHole.m_Direction = HoleParameters.BOTTOM_DIRECTION
    self.m_TopHole = HoleParameters()
    self.m_TopHole.m_Direction = HoleParameters.TOP_DIRECTION
    self.m_TopHole.m_isCreate = False

  def saveToSettings(self,theSett):
    theSett.beginGroup(self.SettSection)
    theSett.setValue("Radius",self.m_StandRadius)
    theSett.setValue("Offset",self.m_StandOffset)
    theSett.setValue("TopLeftCreate",self.m_TopLeftCreate)
    theSett.setValue("TopRightCreate",self.m_TopRightCreate)
    theSett.setValue("BottomLeftCreate",self.m_BottomLeftCreate)
    theSett.setValue("BottomRightCreate",self.m_BottomRightCreate)
    self.m_BottomHole.saveToSettings(theSett,"BottomHole")
    self.m_TopHole.saveToSettings(theSett,"TopHole")
    theSett.endGroup()

  def restoreFromSettings(self,theSett):
    theSett.beginGroup(self.SettSection)
    self.m_StandRadius = float(theSett.value("Radius",4.))
    self.m_StandOffset = float(theSett.value("Offset",-1.5))
    self.m_TopLeftCreate = getSettingsBool(theSett,"TopLeftCreate",True)
    self.m_TopRightCreate = getSettingsBool(theSett,"TopRightCreate",True)
    self.m_BottomLeftCreate = getSettingsBool(theSett,"BottomLeftCreate",True)
    self.m_BottomRightCreate = getSettingsBool(theSett,"BottomRightCreate",True)
    self.m_BottomHole.restoreFromSettings(theSett,"BottomHole")
    self.m_BottomHole.m_Direction = HoleParameters.BOTTOM_DIRECTION
    self.m_TopHole.restoreFromSettings(theSett,"TopHole")
    self.m_TopHole.m_Direction = HoleParameters.TOP_DIRECTION
    theSett.endGroup()

class EnclosureParameters:
  def __init__(self):
    self.m_GeneralParameters = GeneralParameters()
    self.m_EnclosureStandParameters = EnclosureStandParameters()
    self.m_LeftPanel = PanelParameters()
    self.m_RightPanel = PanelParameters()
    self.m_FrontPanel = PanelParameters()
    self.m_FrontPanel.m_Length = 100
    self.m_FrontPanel.m_isCenterPanel = True
    self.m_BackPanel = PanelParameters()
    self.m_BackPanel.m_Length = 100
    self.m_BackPanel.m_isCenterPanel = True
    self.m_CustomStands = []
    self.m_CustomStands.append(CustomStandParameters())
    aCustStand = CustomStandParameters()
    aCustStand.m_X = 70
    aCustStand.m_Y = 20
    aCustStand.m_Hole.m_Direction = HoleParameters.TOP_DIRECTION
    self.m_CustomStands.append(aCustStand)
    self.m_Ears = []

  def saveToFile(self,theFileName):
    aSett = QtCore.QSettings(theFileName, QtCore.QSettings.IniFormat)
    self.save(aSett)
    aSett.sync()
    if aSett.status() != aSett.NoError:
      return False
    return True 

  def saveToSettings(self):
    aSett = QtCore.QSettings(OrganizationName,AppName)
    self.save(aSett)

  def save(self, theSett):
    self.m_GeneralParameters.saveToSettings(theSett)
    self.m_EnclosureStandParameters.saveToSettings(theSett)
    self.m_LeftPanel.saveToSettings(theSett,"LeftPanel")
    self.m_RightPanel.saveToSettings(theSett,"RightPanel")
    self.m_FrontPanel.saveToSettings(theSett,"FrontPanel")
    self.m_BackPanel.saveToSettings(theSett,"BackPanel")
    aCustomStandsCount = len(self.m_CustomStands)
    theSett.setValue("CustomStandsCount",aCustomStandsCount)
    theSett.beginGroup("CustomStands")
    anIndx = 1
    for aCustStand in self.m_CustomStands:
      aGroup = "CustomStand%s" % str(anIndx)
      aCustStand.saveToSettings(theSett,aGroup)
      anIndx = anIndx + 1
    theSett.endGroup()
    anEarsCount = len(self.m_Ears)
    theSett.setValue("EarsCount",anEarsCount)
    theSett.beginGroup("Ears")
    anIndx = 1
    for anEar in self.m_Ears:
      aGroup = "Ear%s" % str(anIndx)
      anEar.saveToSettings(theSett,aGroup)
      anIndx = anIndx + 1
    theSett.endGroup()

  def restoreFromSettings(self):
    aSett = QtCore.QSettings(OrganizationName,AppName)
    self.restore(aSett)

  def openFile(self,theFileName):
    aSett = QtCore.QSettings(theFileName, QtCore.QSettings.IniFormat)
    self.restore(aSett)
    if aSett.status() != aSett.NoError:
      return False
    return True 

  def restore(self,theSett):
    self.m_GeneralParameters.restoreFromSettings(theSett)
    self.m_EnclosureStandParameters.restoreFromSettings(theSett)
    self.m_LeftPanel.restoreFromSettings(theSett,"LeftPanel")
    self.m_RightPanel.restoreFromSettings(theSett,"RightPanel")
    self.m_FrontPanel.restoreFromSettings(theSett,"FrontPanel")
    self.m_BackPanel.restoreFromSettings(theSett,"BackPanel")
    self.m_CustomStands = []
    aCustomStandsCount = int(theSett.value("CustomStandsCount",0))
    theSett.beginGroup("CustomStands")
    for anIndx in range(aCustomStandsCount):
      aCustStand = CustomStandParameters()
      aGroup = "CustomStand%s" % str(anIndx+1)
      aCustStand.restoreFromSettings(theSett,aGroup)
      self.m_CustomStands.append(aCustStand)
    theSett.endGroup()
    self.m_Ears = []
    aCustomStandsCount = int(theSett.value("EarsCount",0))
    theSett.beginGroup("Ears")
    for anIndx in range(aCustomStandsCount):
      anEar = EarParameters()
      aGroup = "Ear%s" % str(anIndx+1)
      anEar.restoreFromSettings(theSett,aGroup)
      self.m_Ears.append(anEar)
    theSett.endGroup()
#For test only
#    aBase = EarParameters.BOTTOM_DIRECTION
#    anEar = EarParameters()
#    anEar.m_Base = aBase
#    anEar.m_Direction = EarParameters.LEFT_DIRECTION
#    anEar.m_Align = EarParameters.FRONT_DIRECTION
#    self.m_Ears.append(anEar)
 
#    anEar = EarParameters()
#    anEar.m_Base = aBase
#    anEar.m_Direction = EarParameters.RIGHT_DIRECTION
#    anEar.m_Align = EarParameters.FRONT_DIRECTION
#    self.m_Ears.append(anEar)

#    anEar = EarParameters()
#    anEar.m_Base = aBase
#    anEar.m_Direction = EarParameters.LEFT_DIRECTION
#    anEar.m_Align = EarParameters.BACK_DIRECTION
#    anEar.m_Width = 15.
#    anEar.m_isCenterHole = False
#    anEar.m_HoleX = 6.
#    anEar.m_HoleY = 6. 
#    self.m_Ears.append(anEar)

#    anEar = EarParameters()
#    anEar.m_Base = aBase
#    anEar.m_Direction = EarParameters.RIGHT_DIRECTION
#    anEar.m_Align = EarParameters.BACK_DIRECTION
#    anEar.m_Width = 15.
#    anEar.m_isCenterHole = False
#    anEar.m_HoleX = 6.
#    anEar.m_HoleY = 6. 
#    self.m_Ears.append(anEar)

#    anEar = EarParameters()
#    anEar.m_Base = EarParameters.BACK_DIRECTION
#    anEar.m_Direction = EarParameters.LEFT_DIRECTION
#    anEar.m_Align = EarParameters.BOTTOM_DIRECTION
#    anEar.m_Width = 15.
#    anEar.m_isCenterHole = False
#    anEar.m_HoleX = 6.
#    anEar.m_HoleY = 9. 
#    self.m_Ears.append(anEar)

#    anEar = EarParameters()
#    anEar.m_Base = EarParameters.BACK_DIRECTION
#    anEar.m_Direction = EarParameters.RIGHT_DIRECTION
#    anEar.m_Align = EarParameters.BOTTOM_DIRECTION
#    anEar.m_Width = 15.
#    anEar.m_isCenterHole = False
#    anEar.m_HoleX = 6.
#    anEar.m_HoleY = 9. 
#    self.m_Ears.append(anEar)

