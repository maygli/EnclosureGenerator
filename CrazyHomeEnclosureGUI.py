# -*- coding: utf-8 -*-

# Macro Begin: D:\3dPrinter\FreeCADMacroses\CrazyHomeEnclosure.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
import os
import FreeCAD
import Part
from PySide import QtGui, QtCore

try:
    from PySide import QtWebKit
    has_qtwebkit = True
except:
    has_qtwebkit = False

from CrazyHomeEnclosureData import *

aCurrDir = os.path.dirname(__file__)
iconsPath = os.path.join( aCurrDir, 'resources' )

class HoleWidget(QtGui.QGroupBox):
  def __init__(self,theTitle,theParent=None):
    QtGui.QGroupBox.__init__(self,theTitle,theParent)
    self.setCheckable(True)                          
    aLayout = QtGui.QGridLayout()

    aRow = 0
    aLayout.addWidget(QtGui.QLabel(self.tr("Hole radius,mm"),self),aRow,0)
    self.m_HoleRadiusLE = QtGui.QLineEdit(self)
    aHoleRadiusVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_HoleRadiusLE)
    self.m_HoleRadiusLE.setValidator(aHoleRadiusVld)
    aLayout.addWidget(self.m_HoleRadiusLE,aRow,1)
 
    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Hole height,mm"),self),aRow,0)
    self.m_HoleHeightLE = QtGui.QLineEdit(self)
    aHoleHeightVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_HoleRadiusLE)
    self.m_HoleHeightLE.setValidator(aHoleHeightVld)
    aLayout.addWidget(self.m_HoleHeightLE,aRow,1)

    aRow = aRow + 1
    self.setLayout(aLayout) 

  def fillParameters(self,theParameters):
    theParameters.m_isCreate = self.isChecked()
    theParameters.m_Radius = float(self.m_HoleRadiusLE.text())
    theParameters.m_Height = float(self.m_HoleHeightLE.text())

  def setParameters(self,theParameters):
    self.setChecked(theParameters.m_isCreate)
    self.m_HoleRadiusLE.setText(str(theParameters.m_Radius))
    self.m_HoleHeightLE.setText(str(theParameters.m_Height))

class HoleParametersDialog(QtGui.QDialog):
  def __init__(self,theHoleParameters,theParent=None):
    QtGui.QDialog.__init__(self,theParent)
    aLayout = QtGui.QVBoxLayout()
    self.m_HoleWidget = HoleWidget(self.tr("Create hole"),self)
    self.m_HoleWidget.setParameters(theHoleParameters)
    aLayout.addWidget(self.m_HoleWidget)
    aDlgBtns = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
    aDlgBtns.accepted.connect(self.accept)
    aDlgBtns.rejected.connect(self.reject)
    aLayout.addWidget(aDlgBtns)
    self.setLayout(aLayout)

  def fillParameters(self, theParameters):
    self.m_HoleWidget.fillParameters(theParameters)

class HoleParametersViewWidget(QtGui.QWidget):
  def __init__(self,theHoleParameters,theParent=None):
    QtGui.QWidget.__init__(self,theParent)
    aLayout = QtGui.QHBoxLayout()
    self.m_Parameters = theHoleParameters
    self.m_StateLabel = QtGui.QLabel(self)
    aLayout.addWidget(self.m_StateLabel)
    anInfoLayout = QtGui.QVBoxLayout()
    anInfoLayout.setSpacing(0)
    anInfoLayout.setContentsMargins(0,0,0,0)
    self.m_RadiusLabel = QtGui.QLabel(self)
    self.m_HeightLabel = QtGui.QLabel(self)
    anInfoLayout.addWidget(self.m_RadiusLabel)
    anInfoLayout.addWidget(self.m_HeightLabel)
    aLayout.addLayout(anInfoLayout)
    self.setData(theHoleParameters)
    anEditIcon = QtGui.QIcon(os.path.join(iconsPath,"edit.png"))
    aBtn = QtGui.QToolButton(self)
    aBtn.setIcon(anEditIcon)
    aBtn.setToolTip(self.tr("Edit hole parameters"))
    aBtn.pressed.connect(self.onEdit)
    aLayout.addWidget(aBtn)
    self.setData(theHoleParameters)
    self.setLayout(aLayout)

  def setData(self,theParameters):
    aStateIconPath = os.path.join(iconsPath,"ok.png")
    if theParameters.m_isCreate == False:
      aStateIconPath = os.path.join(iconsPath,"remove.png")
    aStateIcon = QtGui.QPixmap(aStateIconPath)
    self.m_StateLabel.setPixmap(aStateIconPath)
    aRadiusText = "R=%smm" % theParameters.m_Radius
    aHeightText = "h=%smm" % theParameters.m_Height 
    self.m_RadiusLabel.setText(aRadiusText)
    self.m_HeightLabel.setText(aHeightText)

  def onEdit(self):
    aHoleDlg = HoleParametersDialog(self.m_Parameters,self)
    if aHoleDlg.exec_() == QtGui.QDialog.Accepted:
      aHoleDlg.fillParameters(self.m_Parameters)
      self.setData(self.m_Parameters)

  def getHoleParameters(self):
    return self.m_Parameters

class CustomStandsConfigureTable(QtGui.QTableWidget):
  def __init__(self,theParent=None):
    QtGui.QTableWidget.__init__(self,theParent)
    aColumns = ["Type","X","Y","Radius","Height","Hole"]
    self.setColumnCount(len(aColumns))
    self.setHorizontalHeaderLabels(aColumns)
    self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

  def appendRow(self, theCustomStand):
    aRow = self.rowCount()
    self.insertRow(aRow)
    aColumn = 0
    aComboBox = QtGui.QComboBox(self)
    aComboBox.addItems(["Bottom","Top"])
    if theCustomStand.m_Hole.m_Direction == HoleParameters.BOTTOM_DIRECTION:
      aComboBox.setCurrentIndex(0)                                        
    else:
      aComboBox.setCurrentIndex(1)
    self.setCellWidget(aRow,aColumn,aComboBox)

    aColumn = aColumn + 1
    anXLE = QtGui.QLineEdit(self)
    anXVld = QtGui.QDoubleValidator(0.000001,1000000000.,15,anXLE)
    anXLE.setValidator(anXVld)
    anXLE.setText(str(theCustomStand.m_X))
    self.setCellWidget(aRow,aColumn,anXLE)

    aColumn = aColumn + 1
    anYLE = QtGui.QLineEdit(self)
    anYVld = QtGui.QDoubleValidator(0.000001,1000000000.,15,anYLE)
    anYLE.setValidator(anYVld)
    anYLE.setText(str(theCustomStand.m_Y))
    self.setCellWidget(aRow,aColumn,anYLE)

    aColumn = aColumn + 1
    aRadiusLE = QtGui.QLineEdit(self)
    aRadiusVld = QtGui.QDoubleValidator(0.000001,1000000000.,15,aRadiusLE)
    aRadiusLE.setValidator(aRadiusVld)
    aRadiusLE.setText(str(theCustomStand.m_StandRadius))
    self.setCellWidget(aRow,aColumn,aRadiusLE)

    aColumn = aColumn + 1
    aHeightLE = QtGui.QLineEdit(self)
    aHeightVld = QtGui.QDoubleValidator(0.000001,1000000000.,15,aHeightLE)
    aHeightLE.setValidator(aHeightVld)
    aHeightLE.setText(str(theCustomStand.m_Height))
    self.setCellWidget(aRow,aColumn,aHeightLE)
    
    aColumn = aColumn + 1
    aHoleViewWidget = HoleParametersViewWidget(theCustomStand.m_Hole,self)
    self.setCellWidget(aRow,aColumn,aHoleViewWidget)

    self.resizeRowsToContents()
    self.resizeColumnsToContents()

  def getStands(self):
    aStands = []
    for aRow in range(self.rowCount()):
      aStandPar = CustomStandParameters()

      aColumn = 0;

      aColumn = aColumn + 1
      anXWid = self.cellWidget(aRow,aColumn)
      aStandPar.m_X = float(anXWid.text())
     
      aColumn = aColumn + 1
      anYWid = self.cellWidget(aRow,aColumn)
      aStandPar.m_Y = float(anYWid.text())
 
      aColumn = aColumn + 1
      aRadiusWid = self.cellWidget(aRow,aColumn)
      aStandPar.m_Radius = float(aRadiusWid.text())

      aColumn = aColumn + 1
      aHeightWid = self.cellWidget(aRow,aColumn)
      aStandPar.m_Height = float(aHeightWid.text())

      aColumn = aColumn + 1
      aHoleWid = self.cellWidget(aRow,aColumn)
      aStandPar.m_Hole = aHoleWid.getHoleParameters()

      aColumn = 0
      aDirWid = self.cellWidget(aRow,aColumn)
      if aDirWid.currentIndex() == 0:
        aStandPar.m_Hole.m_Direction = HoleParameters.BOTTOM_DIRECTION
      else:
        aStandPar.m_Hole.m_Direction = HoleParameters.TOP_DIRECTION
 
      aStands.append(aStandPar)
    return aStands

  def removeSelectedRows(self):
    aRows = self.selectionModel().selectedRows()
    for i in range(len(aRows)-1,-1,-1):
      aRow = aRows[i]
      self.removeRow(aRow.row())

  def removeAll(self):
    aRows = self.rowCount()
    for i in range(aRows-1,-1,-1):
      self.removeRow(i)

  def sizeHintForRow(self,theRow):
    aHeight = -1
    for i in range(self.columnCount()):
      aWid = self.cellWidget(theRow, i)
      if aWid is not None:
        aSize = aWid.sizeHint()
        if aHeight < aSize.height():
          aHeight = aSize.height() 
    return aHeight

  def sizeHintForColumn(self,theColumn):
    aWidth = -1
    for i in range(self.rowCount()):
      aWid = self.cellWidget(i,theColumn)
      if aWid is not None:
        aSize = aWid.sizeHint()
        if aWidth < aSize.width():
          aWidth = aSize.width() 
    return aWidth+4

class CustomStandsWidget(QtGui.QWidget):
  def __init__(self,theCustomStands,theParent=None):
    QtGui.QWidget.__init__(self,theParent)
    aLayout = QtGui.QHBoxLayout()
    self.m_TableWidget = CustomStandsConfigureTable(self)
    aBtnsLayout = QtGui.QVBoxLayout()
    anAddBtn = QtGui.QToolButton(self)
    anAddIcon = QtGui.QIcon(os.path.join(iconsPath,"add.png"))
    anAddBtn.setIcon(anAddIcon)
    anAddBtn.setToolTip(self.tr("Add custom stand"))
    anAddBtn.pressed.connect(self.onAdd)
    aBtnsLayout.addWidget(anAddBtn)
    aRemoveBtn = QtGui.QToolButton(self)
    aRemoveIcon = QtGui.QIcon(os.path.join(iconsPath,"remove.png"))
    aRemoveBtn.setIcon(aRemoveIcon)
    aRemoveBtn.setToolTip(self.tr("Remove selected stands"))
    aRemoveBtn.pressed.connect(self.onRemove)
    aBtnsLayout.addWidget(aRemoveBtn)
    aBtnsLayout.addStretch()
    aLayout.addWidget(self.m_TableWidget)
    aLayout.addLayout(aBtnsLayout)
    self.setLayout(aLayout)

  def onRemove(self):
    self.m_TableWidget.removeSelectedRows()

  def onAdd(self):
    aStandParameters = CustomStandParameters()
    self.m_TableWidget.appendRow(aStandParameters)
  
  def getStands(self):
    return self.m_TableWidget.getStands()

  def setStands(self,theCustomStands):
    self.m_TableWidget.removeAll()
    for aCustomStand in theCustomStands:
      self.m_TableWidget.appendRow(aCustomStand)

class EnclosurePanelWidget(QtGui.QGroupBox):
  @QtCore.Slot()
  def upateStates(self):
     self.m_BorderWidthLE.setEnabled(self.m_DefaultBorderWidthChk.isChecked()==False)
     self.m_OffsetLE.setEnabled(self.m_CenterPanelChk.isChecked()==False)

  def __init__(self,theTitle,theParent=None):
    QtGui.QGroupBox.__init__(self,theTitle,theParent)
    self.setCheckable(True)
    aLayout = QtGui.QGridLayout()

    aRow = 0
    aLayout.addWidget(QtGui.QLabel(self.tr("Length,mm"),self),aRow,0)
    self.m_LengthLE = QtGui.QLineEdit(self)
    aLengthVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_LengthLE)
    self.m_LengthLE.setValidator(aLengthVld)
    aLayout.addWidget(self.m_LengthLE,aRow,1)

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Height,mm"),self),aRow,0)
    self.m_HeightLE = QtGui.QLineEdit(self)
    aHeightVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_HeightLE)
    self.m_HeightLE.setValidator(aHeightVld)
    aLayout.addWidget(self.m_HeightLE,aRow,1)

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Center panel horizontally"),self),aRow,0)
    self.m_CenterPanelChk = QtGui.QCheckBox(self)
    self.m_CenterPanelChk.toggled.connect(self.upateStates)
    aLayout.addWidget(self.m_CenterPanelChk,aRow,1)

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Horizontal offset,mm"),self),aRow,0)
    self.m_OffsetLE = QtGui.QLineEdit(self)
    aOffsetVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_OffsetLE)
    self.m_OffsetLE.setValidator(aOffsetVld)
    aLayout.addWidget(self.m_OffsetLE,aRow,1)

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Border height,mm"),self),aRow,0)
    self.m_BorderHeightLE = QtGui.QLineEdit(self)
    aBorderHeightVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_BorderHeightLE)
    self.m_BorderHeightLE.setValidator(aBorderHeightVld)
    aLayout.addWidget(self.m_BorderHeightLE,aRow,1)

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Default border width"),self),aRow,0)
    self.m_DefaultBorderWidthChk = QtGui.QCheckBox(self)
    aLayout.addWidget(self.m_DefaultBorderWidthChk,aRow,1)
    self.m_DefaultBorderWidthChk.toggled.connect(self.upateStates)

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Border width,mm"),self),aRow,0)
    self.m_BorderWidthLE = QtGui.QLineEdit(self)
    aBorderWidthVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_BorderWidthLE)
    self.m_BorderWidthLE.setValidator(aBorderWidthVld)
    aLayout.addWidget(self.m_BorderWidthLE,aRow,1)

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Simplify panel"),self),aRow,0)
    self.m_SimplifyPanelChk = QtGui.QCheckBox(self)
    aLayout.addWidget(self.m_SimplifyPanelChk,aRow,1)

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Reduce border width,mm"),self),aRow,0)
    self.m_ReduceBorderWidthLE = QtGui.QLineEdit(self)
    aReduceBorderWidthVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_ReduceBorderWidthLE)
    self.m_ReduceBorderWidthLE.setValidator(aReduceBorderWidthVld)
    aLayout.addWidget(self.m_ReduceBorderWidthLE,aRow,1)

    self.setLayout(aLayout)
    self.upateStates()

  def fillParameters(self, theParameters):
    theParameters.m_isCreate = self.isChecked()
    theParameters.m_Length = float(self.m_LengthLE.text())
    theParameters.m_Height = float(self.m_HeightLE.text())
    theParameters.m_isCenterPanel = self.m_CenterPanelChk.isChecked()
    theParameters.m_Offset = float(self.m_OffsetLE.text())
    theParameters.m_BorderHeight = float(self.m_BorderHeightLE.text())
    theParameters.m_isDefaultBorderWidth = self.m_DefaultBorderWidthChk.isChecked()
    theParameters.m_BorderWidth = float(self.m_BorderWidthLE.text())
    theParameters.m_isCreateSimplePanel = self.m_SimplifyPanelChk.isChecked()
    theParameters.m_BorderWidthReduce = float(self.m_ReduceBorderWidthLE.text())


  def setParameters(self, theParameters):
    self.setChecked(theParameters.m_isCreate) 
    self.m_LengthLE.setText(str(theParameters.m_Length))
    self.m_HeightLE.setText(str(theParameters.m_Height))
    self.m_CenterPanelChk.setChecked(theParameters.m_isCenterPanel)
    self.m_OffsetLE.setText(str(theParameters.m_Offset))
    self.m_BorderHeightLE.setText(str(theParameters.m_BorderHeight))
    self.m_DefaultBorderWidthChk.setChecked(theParameters.m_isDefaultBorderWidth)
    self.m_BorderWidthLE.setText(str(theParameters.m_BorderWidth))
    self.m_SimplifyPanelChk.setChecked(theParameters.m_isCreateSimplePanel)
    self.m_ReduceBorderWidthLE.setText(str(theParameters.m_BorderWidthReduce))
    self.upateStates()
  
class EnclosureControlPanel(QtGui.QDialog):

  def __init__(self,theParent=None):
    QtGui.QDialog.__init__(self,theParent)
    self.m_FileName = None

    aLayout = QtGui.QVBoxLayout()

    aTabLayout = QtGui.QHBoxLayout()
    aToolBar = self.createToolBar()

    aTabLayout.addWidget(aToolBar)

    aSplitter = QtGui.QSplitter(self)

    aTabWidget = QtGui.QTabWidget(self)

    aBasicTab = self.createGeneralPanel(aTabWidget)
    aTabWidget.addTab(aBasicTab,self.tr("General")) 

    anEnclosureStandPanel = self.createEnclosureStandPanel(aTabWidget)
    aTabWidget.addTab(anEnclosureStandPanel,self.tr("Enclosure stands")) 

    self.m_CustomStandsWidget = CustomStandsWidget(self)
    aTabWidget.addTab(self.m_CustomStandsWidget,self.tr("Custom stands")) 
    
    self.m_LeftPanelWidget = EnclosurePanelWidget(self.tr("Create panel"),aTabWidget)   
    aTabWidget.addTab(self.m_LeftPanelWidget,self.tr("Left panel")) 

    self.m_RightPanelWidget = EnclosurePanelWidget(self.tr("Create panel"),aTabWidget)   
    aTabWidget.addTab(self.m_RightPanelWidget,self.tr("Right panel")) 

    self.m_FrontPanelWidget = EnclosurePanelWidget(self.tr("Create panel"),aTabWidget)   
    aTabWidget.addTab(self.m_FrontPanelWidget,self.tr("Front panel")) 

    self.m_BackPanelWidget = EnclosurePanelWidget(self.tr("Create panel"),aTabWidget)   
    aTabWidget.addTab(self.m_BackPanelWidget,self.tr("Back panel")) 

    aSplitter.addWidget(aTabWidget)

    if(has_qtwebkit):
        self.m_HelpWdg = QtWebKit.QWebView(self)
        self.m_HelpWdg.load(QtCore.QUrl("http://www.google.com"))
        aSplitter.addWidget(self.m_HelpWdg)
        aTabLayout.addWidget(aSplitter)

    aLayout.addLayout(aTabLayout)
    aDlgBtns = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
    aDlgBtns.accepted.connect(self.accept)
    aDlgBtns.rejected.connect(self.reject)
    aLayout.addWidget(aDlgBtns)
    self.setLayout(aLayout)
    self.setTitle()
    if(has_qtwebkit):
        self.onHelp()
#    self.onSaveAs()

  def createToolBar(self):
    aToolBar = QtGui.QToolBar(self)

    aToolBar.setOrientation(QtCore.Qt.Vertical)
    anOpenBtn = QtGui.QToolButton(self)
    anOpenIcon = QtGui.QIcon(os.path.join(iconsPath,"open.png"))
    anOpenBtn.setIcon(anOpenIcon)
    anOpenBtn.setToolTip(self.tr("Open enclosure parameters file"))
#    anOpenBtn.triggered.connect(self.onOpen)
    aToolBar.addWidget(anOpenBtn)

    aSaveBtn = QtGui.QToolButton(self)
    aSaveIcon = QtGui.QIcon(os.path.join(iconsPath,"save.png"))
    aSaveBtn.setIcon(aSaveIcon)
    aSaveBtn.setToolTip(self.tr("Save enclosure parameters to file"))
    aSaveBtn.clicked.connect(self.onSave)
    aToolBar.addWidget(aSaveBtn)

    aSaveAsBtn = QtGui.QToolButton(self)
    aSaveAsIcon = QtGui.QIcon(os.path.join(iconsPath,"saveas.png"))
    aSaveAsBtn.setIcon(aSaveAsIcon)
    aSaveAsBtn.setToolTip(self.tr("Save enclosure parameters as"))
    aSaveAsBtn.clicked.connect(self.onSaveAs)
    aToolBar.addWidget(aSaveAsBtn)

    aRevertBtn = QtGui.QToolButton(self)
    aRevertIcon = QtGui.QIcon(os.path.join(iconsPath,"reset.png"))
    aRevertBtn.setIcon(aRevertIcon)
    aRevertBtn.setToolTip(self.tr("Revert parameters to last saved"))
    aRevertBtn.clicked.connect(self.onRevert)
    aToolBar.addWidget(aRevertBtn)

    aClearBtn = QtGui.QToolButton(self)
    aClearIcon = QtGui.QIcon(os.path.join(iconsPath,"clear.png"))
    aClearBtn.setIcon(aClearIcon)
    aClearBtn.setToolTip(self.tr("Default parameters"))
    aClearBtn.clicked.connect(self.onClear)
    aToolBar.addWidget(aClearBtn)

    self.m_HelpBtn = QtGui.QToolButton(self)
    aHelpIcon = QtGui.QIcon(os.path.join(iconsPath,"help.png"))
    self.m_HelpBtn.setIcon(aHelpIcon)
    self.m_HelpBtn.setToolTip(self.tr("Help"))
    self.m_HelpBtn.setCheckable(True)
    aToolBar.addWidget(self.m_HelpBtn)
    self.m_HelpBtn.toggled.connect(self.onHelp)

    return aToolBar

  def createEnclosureStandPanel(self,theParent=None):
    aBasicPanel = QtGui.QWidget(theParent)
    aLayout = QtGui.QGridLayout()

    aRow = 0
    aLayout.addWidget(QtGui.QLabel(self.tr("Stand radius,mm"),aBasicPanel),aRow,0)
    self.m_StandRadiusLE = QtGui.QLineEdit(aBasicPanel)
    aStandRadiusVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_StandRadiusLE)
    self.m_StandRadiusLE.setValidator(aStandRadiusVld)
    aLayout.addWidget(self.m_StandRadiusLE,aRow,1) 

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Stand offset from border,mm"),aBasicPanel),aRow,0)
    self.m_StandOffsetLE = QtGui.QLineEdit(aBasicPanel)
    aStandOffsetVld = QtGui.QDoubleValidator(-1000000000,1000000000.,15,self.m_StandOffsetLE)
    self.m_StandOffsetLE.setValidator(aStandRadiusVld)
    aLayout.addWidget(self.m_StandOffsetLE,aRow,1) 

    aRow = aRow+1
    aLayout.addWidget(QtGui.QLabel(self.tr("Bottom left stand,mm"),aBasicPanel),aRow,0)
    self.m_BottomLeftChk = QtGui.QCheckBox(aBasicPanel)
    aLayout.addWidget(self.m_BottomLeftChk,aRow,1)

    aRow = aRow+1
    aLayout.addWidget(QtGui.QLabel(self.tr("Bottom right stand,mm"),aBasicPanel),aRow,0)
    self.m_BottomRightChk = QtGui.QCheckBox(aBasicPanel)
    aLayout.addWidget(self.m_BottomRightChk,aRow,1)

    aRow = aRow+1
    aLayout.addWidget(QtGui.QLabel(self.tr("Top left stand,mm"),aBasicPanel),aRow,0)
    self.m_TopLeftChk = QtGui.QCheckBox(aBasicPanel)
    aLayout.addWidget(self.m_TopLeftChk,aRow,1)

    aRow = aRow+1
    aLayout.addWidget(QtGui.QLabel(self.tr("Top right stand,mm"),aBasicPanel),aRow,0)
    self.m_TopRightChk = QtGui.QCheckBox(aBasicPanel)
    aLayout.addWidget(self.m_TopRightChk,aRow,1)

    aRow = aRow+1
    self.m_BottomHoleWdg = HoleWidget(self.tr("Bottom hole"),aBasicPanel)
    aLayout.addWidget(self.m_BottomHoleWdg,aRow,0,1,2)

    aRow = aRow+1
    self.m_TopHoleWdg = HoleWidget(self.tr("Top hole"),aBasicPanel)
    aLayout.addWidget(self.m_TopHoleWdg,aRow,0,1,2)

    aBasicPanel.setLayout(aLayout)
    return aBasicPanel

  def createGeneralPanel(self,theParent=None):
    aBasicPanel = QtGui.QWidget(theParent)
    aLayout = QtGui.QGridLayout()

    aRow = 0
    aLayout.addWidget(QtGui.QLabel(self.tr("Lenght,mm"),aBasicPanel),aRow,0)
    self.m_LenghtLE = QtGui.QLineEdit(aBasicPanel)
    aLenghtVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_LenghtLE)
    self.m_LenghtLE.setValidator(aLenghtVld)
    aLayout.addWidget(self.m_LenghtLE,aRow,1) 

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Width,mm"),aBasicPanel),aRow,0)
    self.m_WidthLE = QtGui.QLineEdit(aBasicPanel)
    aWidthVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_WidthLE)
    self.m_WidthLE.setValidator(aWidthVld)
    aLayout.addWidget(self.m_WidthLE,aRow,1) 

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Height,mm"),aBasicPanel),aRow,0)
    self.m_HeightLE = QtGui.QLineEdit(aBasicPanel)
    aHeightVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_HeightLE)
    self.m_HeightLE.setValidator(aHeightVld)
    aLayout.addWidget(self.m_HeightLE,aRow,1) 

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Bottom height,mm"),aBasicPanel),aRow,0)
    self.m_BottomHeightLE = QtGui.QLineEdit(aBasicPanel)
    aBottomHeightVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_BottomHeightLE)
    self.m_BottomHeightLE.setValidator(aBottomHeightVld)
    aLayout.addWidget(self.m_BottomHeightLE,aRow,1) 

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Notch height,mm"),aBasicPanel),aRow,0)
    self.m_NotchHeightLE = QtGui.QLineEdit(aBasicPanel)
    aNotchHeightVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_NotchHeightLE)
    self.m_NotchHeightLE.setValidator(aNotchHeightVld)
    aLayout.addWidget(self.m_NotchHeightLE,aRow,1) 

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Horizontal border height,mm"),aBasicPanel),aRow,0)
    self.m_HBorderHeightLE = QtGui.QLineEdit(aBasicPanel)
    aHBorderHeightVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_HBorderHeightLE)
    self.m_HBorderHeightLE.setValidator(aHBorderHeightVld)
    aLayout.addWidget(self.m_HBorderHeightLE,aRow,1) 

    aRow = aRow + 1
    aLayout.addWidget(QtGui.QLabel(self.tr("Vertical border width,mm"),aBasicPanel),aRow,0)
    self.m_VBorderWidthLE = QtGui.QLineEdit(aBasicPanel)
    aVBorderWidthVld = QtGui.QDoubleValidator(0.0001,1000000000.,15,self.m_VBorderWidthLE)
    self.m_VBorderWidthLE.setValidator(aVBorderWidthVld)
    aLayout.addWidget(self.m_VBorderWidthLE,aRow,1) 

    aBasicPanel.setLayout(aLayout)
    return aBasicPanel

  def fillParameters(self, theParameters):
    theParameters.m_GeneralParameters.m_Length = float(self.m_LenghtLE.text())
    theParameters.m_GeneralParameters.m_Width = float(self.m_WidthLE.text())
    theParameters.m_GeneralParameters.m_TotalHeight = float(self.m_HeightLE.text())
    theParameters.m_GeneralParameters.m_BottomHeight = float(self.m_BottomHeightLE.text())
    theParameters.m_GeneralParameters.m_NotchHeight = float(self.m_NotchHeightLE.text())
    theParameters.m_GeneralParameters.m_HorizontalBorderWidth = float(self.m_HBorderHeightLE.text())
    theParameters.m_GeneralParameters.m_VerticalBorderWidth = float(self.m_VBorderWidthLE.text())
    theParameters.m_EnclosureStandParameters.m_StandRaius = float(self.m_StandRadiusLE.text())
    theParameters.m_EnclosureStandParameters.m_StandOffset = float(self.m_StandOffsetLE.text())
    theParameters.m_EnclosureStandParameters.m_TopLeftCreate = self.m_TopLeftChk.isChecked()
    theParameters.m_EnclosureStandParameters.m_TopRightCreate = self.m_TopRightChk.isChecked()
    theParameters.m_EnclosureStandParameters.m_BottomLeftCreate = self.m_BottomLeftChk.isChecked()
    theParameters.m_EnclosureStandParameters.m_BottomRightCreate = self.m_BottomRightChk.isChecked()
    theParameters.m_CustomStands = self.m_CustomStandsWidget.getStands()
    self.m_BottomHoleWdg.fillParameters(theParameters.m_EnclosureStandParameters.m_BottomHole)
    self.m_TopHoleWdg.fillParameters(theParameters.m_EnclosureStandParameters.m_TopHole)
    self.m_LeftPanelWidget.fillParameters(theParameters.m_LeftPanel)
    self.m_RightPanelWidget.fillParameters(theParameters.m_RightPanel)
    self.m_FrontPanelWidget.fillParameters(theParameters.m_FrontPanel)
    self.m_BackPanelWidget.fillParameters(theParameters.m_BackPanel)

  def setParameters(self,theParameters):
    self.m_LenghtLE.setText(str(theParameters.m_GeneralParameters.m_Length))
    self.m_WidthLE.setText(str(theParameters.m_GeneralParameters.m_Width))
    self.m_HeightLE.setText(str(theParameters.m_GeneralParameters.m_TotalHeight))
    self.m_BottomHeightLE.setText(str(theParameters.m_GeneralParameters.m_BottomHeight))
    self.m_NotchHeightLE.setText(str(theParameters.m_GeneralParameters.m_NotchHeight))
    self.m_HBorderHeightLE.setText(str(theParameters.m_GeneralParameters.m_HorizontalBorderWidth))
    self.m_VBorderWidthLE.setText(str(theParameters.m_GeneralParameters.m_VerticalBorderWidth))
    self.m_StandRadiusLE.setText(str(theParameters.m_EnclosureStandParameters.m_StandRadius))
    self.m_StandOffsetLE.setText(str(theParameters.m_EnclosureStandParameters.m_StandOffset))
    self.m_TopLeftChk.setChecked(theParameters.m_EnclosureStandParameters.m_TopLeftCreate)
    self.m_TopRightChk.setChecked(theParameters.m_EnclosureStandParameters.m_TopRightCreate)
    self.m_BottomLeftChk.setChecked(theParameters.m_EnclosureStandParameters.m_BottomLeftCreate)
    self.m_BottomRightChk.setChecked(theParameters.m_EnclosureStandParameters.m_BottomRightCreate)
    self.m_CustomStandsWidget.setStands(theParameters.m_CustomStands)
    self.m_BottomHoleWdg.setParameters(theParameters.m_EnclosureStandParameters.m_BottomHole)
    self.m_TopHoleWdg.setParameters(theParameters.m_EnclosureStandParameters.m_TopHole)
    self.m_LeftPanelWidget.setParameters(theParameters.m_LeftPanel)
    self.m_RightPanelWidget.setParameters(theParameters.m_RightPanel)
    self.m_FrontPanelWidget.setParameters(theParameters.m_FrontPanel)
    self.m_BackPanelWidget.setParameters(theParameters.m_BackPanel)

  def setTitle(self):
    aFileName = self.m_FileName
    if aFileName is None:
      aFileName = "Untitled"
    aTitle = "%s - Enclosure generator" % aFileName
    self.setWindowTitle(aTitle)
 
  def saveToFile(self,theFileName):
    aParameters = EnclosureParameters()
    self.fillParameters(aParameters)
    print "Save to file %s" % theFileName
    aRes = aParameters.saveToFile(theFileName)
    if aRes != True:
      QtGui.QMessageBox.critical(self,"Can't save enclosure parameters","Can't save enclosure parameters to file %s" % theFileName)
    else:
      self.m_FileName = theFileName
      self.setTitle()

  @QtCore.Slot()
  def onSave(self):
    print "onSave"
    if self.m_FileName is None:
      self.onSaveAs()
      return
    self.saveToFile(self.m_FileName)
    
  @QtCore.Slot()
  def onSaveAs(self):
    aFileName, aFilter = QtGui.QFileDialog.getSaveFileName(self,"Save enclosure parameters","","Enclosure parameters (*.enc);;All files(*)")
    if not aFileName:
      print "File name empty " + aFileName 
      return
    self.saveToFile(aFileName)      

  def onOpen(self):
    pass

  def onRevert(self):
    aParameters = EnclosureParameters()
    aParameters.restoreFromSettings()
    self.setParameters(aParameters)
    pass

  def onClear(self):
    aParameters = EnclosureParameters()
    self.setParameters(aParameters)
    pass

  def onHelp(self):
    self.m_HelpWdg.setVisible(self.m_HelpBtn.isChecked())
    pass
