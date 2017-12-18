import FreeCAD
from CrazyHomeEnclosureData import * 

class EnclosureGenerator:
  def __init__(self,theParameters,theParent=None):
    self.m_Parameters = theParameters

  def generate(self):
    aBottomBase = self.createBottomBase()
    aTopBase = self.createTopBase(aBottomBase)
    aLeftX = self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth + self.m_Parameters.m_EnclosureStandParameters.m_StandRadius + self.m_Parameters.m_EnclosureStandParameters.m_StandOffset
    aBottomY = aLeftX
    aRightX = self.m_Parameters.m_GeneralParameters.m_Length - aLeftX 
    aTopY = self.m_Parameters.m_GeneralParameters.m_Width - aBottomY
    anEcnlosureStandRadius = self.m_Parameters.m_EnclosureStandParameters.m_StandRadius 
    aBottomStandHeight = self.m_Parameters.m_GeneralParameters.m_BottomHeight - self.m_Parameters.m_GeneralParameters.m_NotchHeight - self.m_Parameters.m_GeneralParameters.m_HorizontalBorderWidth
    aTopStandHeight = self.m_Parameters.m_GeneralParameters.m_TotalHeight - self.m_Parameters.m_GeneralParameters.m_BottomHeight - self.m_Parameters.m_GeneralParameters.m_HorizontalBorderWidth
    anIndx = 1
    if self.m_Parameters.m_EnclosureStandParameters.m_TopLeftCreate:
      aBottomBase = self.createVerticalStand(aBottomBase,True,anIndx,aLeftX,aTopY,"EnclosureStandBottomBackLeft",anEcnlosureStandRadius,
                                             aBottomStandHeight, self.m_Parameters.m_EnclosureStandParameters.m_BottomHole)
      aTopBase = self.createVerticalStand(aTopBase,False,anIndx,aLeftX,aTopY,"EnclosureStandTopBackLeft",anEcnlosureStandRadius,
                                             aTopStandHeight,self.m_Parameters.m_EnclosureStandParameters.m_TopHole)
      anIndx = anIndx+1
    if self.m_Parameters.m_EnclosureStandParameters.m_TopRightCreate:
      aBottomBase = self.createVerticalStand(aBottomBase,True,anIndx,aRightX,aTopY,"EnclosureStandBottomBackRight",anEcnlosureStandRadius,
                                             aBottomStandHeight,self.m_Parameters.m_EnclosureStandParameters.m_BottomHole)
      aTopBase = self.createVerticalStand(aTopBase,False,anIndx,aRightX,aTopY,"EnclosureStandTopBackRight",anEcnlosureStandRadius,
                                            aTopStandHeight,self.m_Parameters.m_EnclosureStandParameters.m_TopHole)
      anIndx = anIndx+1
    if self.m_Parameters.m_EnclosureStandParameters.m_BottomLeftCreate:
      aBottomBase = self.createVerticalStand(aBottomBase,True,anIndx,aLeftX,aBottomY,"EnclosureStandBottomFrontLeft",anEcnlosureStandRadius,
                                             aBottomStandHeight,self.m_Parameters.m_EnclosureStandParameters.m_BottomHole)
      aTopBase = self.createVerticalStand(aTopBase,False,anIndx,aLeftX,aBottomY,"EnclosureStandTopFrontLeft",anEcnlosureStandRadius,
                                            aTopStandHeight,self.m_Parameters.m_EnclosureStandParameters.m_TopHole)
      anIndx = anIndx+1
    if self.m_Parameters.m_EnclosureStandParameters.m_BottomRightCreate:
      aBottomBase = self.createVerticalStand(aBottomBase,True,anIndx,aRightX,aBottomY,"EnclosureStandBottomFrontRight",anEcnlosureStandRadius,
                                            aBottomStandHeight,self.m_Parameters.m_EnclosureStandParameters.m_BottomHole)
      aTopBase = self.createVerticalStand(aTopBase,False,anIndx,aRightX,aBottomY,"EnclosureStandTopFrontRight",anEcnlosureStandRadius,
                                            aTopStandHeight,self.m_Parameters.m_EnclosureStandParameters.m_TopHole)
      anIndx = anIndx+1
    aTopBase, aBottomBase = self.createLeftRightPanel( aTopBase, aBottomBase, "LeftPanel", self.m_Parameters.m_LeftPanel, True, True)
    aTopBase, aBottomBase = self.createLeftRightPanel( aTopBase, aBottomBase, "RightPanel", self.m_Parameters.m_RightPanel, False, True)
    aTopBase, aBottomBase = self.createFrontBackPanel( aTopBase, aBottomBase, "FrontPanel", self.m_Parameters.m_FrontPanel, True, True)
    aTopBase, aBottomBase = self.createFrontBackPanel( aTopBase, aBottomBase, "BackPanel", self.m_Parameters.m_BackPanel, False, True)
    aTopBase, aBottomBase = self.createLeftRightPanel( aTopBase, aBottomBase, "LeftPanel", self.m_Parameters.m_LeftPanel, True, False)
    aTopBase, aBottomBase = self.createLeftRightPanel( aTopBase, aBottomBase, "RightPanel", self.m_Parameters.m_RightPanel, False, False)
    aTopBase, aBottomBase = self.createFrontBackPanel( aTopBase, aBottomBase, "FrontPanel", self.m_Parameters.m_FrontPanel, True, False)
    aTopBase, aBottomBase = self.createFrontBackPanel( aTopBase, aBottomBase, "BackPanel", self.m_Parameters.m_BackPanel, False, False)
    anIndx = 1
    for aCustomStand in self.m_Parameters.m_CustomStands:
      aTopBase,aBottomBase = self.createVerticalCustomStand(aTopBase,aBottomBase,anIndx,aCustomStand)
      anIndx = anIndx + 1
    FreeCAD.ActiveDocument.recompute()
                                                                                                                      
  def getInmm(self,theVal):                                                                                            
    return str(theVal) + " mm"

  def cutObjects(self, theBase, theTool, theLabel):
    aCut = FreeCAD.ActiveDocument.addObject("Part::Cut","Cut")
    aCut.Label = theLabel
    FreeCAD.ActiveDocument.recompute()
    aCut.Base = theBase
    aCut.Tool = theTool
    theBase.ViewObject.Visibility=False
    theTool.ViewObject.Visibility=False
    aCut.ViewObject.ShapeColor=theBase.ViewObject.ShapeColor
    aCut.ViewObject.DisplayMode=theBase.ViewObject.DisplayMode
    return aCut

  def joinObjects(self,theObjects,theLabel):
    aFusion = FreeCAD.activeDocument().addObject("Part::MultiFuse","Fusion")
    aFusion.Label = theLabel
    aFusion.Shapes = theObjects
    for anObject in theObjects:
      anObject.ViewObject.Visibility=False
    aFusion.ViewObject.ShapeColor=theObjects[0].ViewObject.ShapeColor
    aFusion.ViewObject.DisplayMode=theObjects[0].ViewObject.DisplayMode
    return aFusion

  def createBox(self, theLength, theWidth, theHeight, theX, theY, theZ, theLabel):
    aBox = FreeCAD.ActiveDocument.addObject("Part::Box","Box")
    aBox.Label = theLabel
    FreeCAD.ActiveDocument.recompute()
    aBox.Length = theLength
    aBox.Width = theWidth
    aBox.Height = theHeight
    aBox.Placement.Base.x = theX
    aBox.Placement.Base.y = theY
    aBox.Placement.Base.z = theZ
    return aBox
 
  def createCylinder(self, theRadius, theHeight, theX, theY, theZ, theLabel):
    aCylinder = FreeCAD.ActiveDocument.addObject("Part::Cylinder","Cylinder")
    aCylinder.Label = theLabel
    FreeCAD.ActiveDocument.recompute()
    aCylinder.Radius = theRadius 
    aCylinder.Height = theHeight
    aCylinder.Placement.Base.x = theX
    aCylinder.Placement.Base.y = theY
    aCylinder.Placement.Base.z = theZ
    return aCylinder

  def roundBoxLeftRight(self,theBox,thePrefix,theRadius):
    aFillet = FreeCAD.ActiveDocument.addObject("Part::Fillet","Fillet")
    aFillet.Base = theBox
    aFillet.Label = thePrefix
    aFillets = []
    aFillets.append((9,theRadius,theRadius))
    aFillets.append((10,theRadius,theRadius))
    aFillets.append((11,theRadius,theRadius))
    aFillets.append((12,theRadius,theRadius))
    aFillet.Edges = aFillets
    del aFillets
    theBox.ViewObject.Visibility = False
    return aFillet

  def roundBoxFrontBack(self,theBox,thePrefix,theRadius):
    aFillet = FreeCAD.ActiveDocument.addObject("Part::Fillet","Fillet")
    aFillet.Base = theBox
    aFillet.Label = thePrefix
    aFillets = []
    aFillets.append((2,theRadius,theRadius))
    aFillets.append((4,theRadius,theRadius))
    aFillets.append((6,theRadius,theRadius))
    aFillets.append((8,theRadius,theRadius))
    aFillet.Edges = aFillets
    del aFillets
    theBox.ViewObject.Visibility = False
    return aFillet

  def createBottomBase(self):
    aBottomExternal = self.createBox(self.m_Parameters.m_GeneralParameters.m_Length,self.m_Parameters.m_GeneralParameters.m_Width,
                                     self.m_Parameters.m_GeneralParameters.m_BottomHeight+self.m_Parameters.m_GeneralParameters.m_NotchHeight,
                                     0,0,0,"BottomExternal")
 
    aBottomInternal = self.createBox(self.m_Parameters.m_GeneralParameters.m_Length-2*self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
                                     self.m_Parameters.m_GeneralParameters.m_Width-2*self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
                                     self.m_Parameters.m_GeneralParameters.m_BottomHeight+self.m_Parameters.m_GeneralParameters.m_NotchHeight,
                                     self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
                                     self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
                                     self.m_Parameters.m_GeneralParameters.m_HorizontalBorderWidth, 
                                     "BottomInternal")

    aCut = self.cutObjects(aBottomExternal,aBottomInternal,"BottomBase")

    aBottomNotchRemoval = self.createBox(self.m_Parameters.m_GeneralParameters.m_Length-self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
                                         self.m_Parameters.m_GeneralParameters.m_Width-self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
                                         self.m_Parameters.m_GeneralParameters.m_BottomHeight,
                                         self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth/2,
                                         self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth/2.,
                                         self.m_Parameters.m_GeneralParameters.m_BottomHeight-self.m_Parameters.m_GeneralParameters.m_NotchHeight,
                                         "BottomRemoval" )

    aCut1 = self.cutObjects(aCut,aBottomNotchRemoval,"BottomNotchBase")

    return aCut1

  def createTopBase( self,theBottomBase ):
    aTopHeight = self.m_Parameters.m_GeneralParameters.m_TotalHeight-self.m_Parameters.m_GeneralParameters.m_BottomHeight

    aTopExternal = self.createBox(self.m_Parameters.m_GeneralParameters.m_Length,
                                  self.m_Parameters.m_GeneralParameters.m_Width,
                                  aTopHeight+self.m_Parameters.m_GeneralParameters.m_NotchHeight,
                                  0,0, 
                                  self.m_Parameters.m_GeneralParameters.m_TotalHeight - aTopHeight - self.m_Parameters.m_GeneralParameters.m_NotchHeight,
                                  "TopExternal")

    aTopInternal = self.createBox(self.m_Parameters.m_GeneralParameters.m_Length-2.*self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
                                  self.m_Parameters.m_GeneralParameters.m_Width-2.*self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
				  aTopExternal.Height,
                                  self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
                                  self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth,
                                  aTopExternal.Placement.Base.z - self.m_Parameters.m_GeneralParameters.m_HorizontalBorderWidth,
                                  "TopInternal")
    aBaseCut = self.cutObjects(aTopExternal,aTopInternal,"TopBase")

    aBottomCopy = FreeCAD.ActiveDocument.copyObject(theBottomBase,False)   

    aNotchCut = self.cutObjects(aBaseCut,aBottomCopy,"TopNotchBase")
    return aNotchCut

  def createVerticalCustomStand( self, theTopBase, theBottomBase, theIndx, theParameters ):
#    self.m_StandRadius = 4.
#    self.m_Height = 2.
#    self.m_X = 30.
#    self.m_Y = 30.
#    self.m_Hole = HoleParameters()
    aTopBase = theTopBase
    aBottomBase = theBottomBase
    isBottom = True
    if theParameters.m_Hole.m_Direction == HoleParameters.BOTTOM_DIRECTION:
      aBottomBase = self.createVerticalStand(aBottomBase, True, theIndx, theParameters.m_X, theParameters.m_Y, "CustomStandBottom",
                             theParameters.m_StandRadius, theParameters.m_Height, theParameters.m_Hole)
    else:
      aTopBase = self.createVerticalStand(aTopBase, False, theIndx, theParameters.m_X, theParameters.m_Y, "CustomStandTop",
                             theParameters.m_StandRadius, theParameters.m_Height, theParameters.m_Hole)
    return aTopBase, aBottomBase

  def createVerticalStand(self,theBase,isBottom,theIndx,theX,theY,thePrefix,theRadius,theHeight,theHoleParameters):
    aHeight = theHeight
    aZ = 0
    if isBottom:
      aZ = self.m_Parameters.m_GeneralParameters.m_HorizontalBorderWidth
      if self.m_Parameters.m_GeneralParameters.m_HorizontalBorderWidth > 0.5:
        aZ = aZ - 0.5
        aHeight = aHeight + 0.5  
    else:
      aZ = self.m_Parameters.m_GeneralParameters.m_TotalHeight - self.m_Parameters.m_GeneralParameters.m_HorizontalBorderWidth - theHeight
      if self.m_Parameters.m_GeneralParameters.m_HorizontalBorderWidth > 0.5:
        aHeight = aHeight + 0.5  
      
    aStand = self.createCylinder(self.m_Parameters.m_EnclosureStandParameters.m_StandRadius,aHeight,theX,theY,aZ,thePrefix)

    aFusionLabel = thePrefix+"Base"+str(theIndx)
    aFusion = self.joinObjects([theBase,aStand],aFusionLabel)
    if isBottom:
      aResult = self.createHole(aFusion,theX,theY,aZ+aHeight,thePrefix+"BaseHole",theHoleParameters)
    else:
      aResult = self.createHole(aFusion,theX,theY,aZ,thePrefix+"BaseHole",theHoleParameters)
    return aResult

  def createHole(self, theBase, theX, theY, theZ, thePrefix, theHoleParameters):
    if theHoleParameters.m_isCreate == False:
      return theBase
    aZ = theZ
    if theHoleParameters.m_Direction == HoleParameters.BOTTOM_DIRECTION:
      aZ = theZ - theHoleParameters.m_Height
    aHole = self.createCylinder(theHoleParameters.m_Radius,theHoleParameters.m_Height,theX,theY,aZ,thePrefix)

    aBaseCut = self.cutObjects(theBase,aHole,thePrefix + "Cut")

    return aBaseCut
      
  def createFrontBackPanel(self, theTopBase, theBottomBase, theTitle, theParameters, isFront, isHole):
#    self.m_isCreate = True
#    self.m_Length = 26.
#    self.m_Height = 18.
#    self.m_isCenterPanel = False
#    self.m_Offset = 52.
#    self.m_BorderHeight = 1.5
#    self.m_isDefaultBorderWidth = True
#    self.m_BorderWidth = 1.
#    self.m_isCreateSimplePanel = True
#    self.m_BorderWidthReduce = 0.2
    if theParameters.m_isCreate==False:
      return theTopBase, theBottomBase
    aLabelPostfix = ""
    aBorderWidth = theParameters.m_BorderWidth
    if theParameters.m_isDefaultBorderWidth:
      aBorderWidth = self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth/3
    anInternalWidth = self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth
    anExternalOffset = (self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth - aBorderWidth)/2
    anInternalOffset = 0.
    if isHole:
      aLabelPostfix = "Hole"
    else:
      aBorderWidth = aBorderWidth - theParameters.m_BorderWidthReduce
      anExternalOffset = anExternalOffset + theParameters.m_BorderWidthReduce/2.
      if theParameters.m_isCreateSimplePanel:
        anInternalWidth = anExternalOffset + aBorderWidth - 0.00001
        if not isFront:
#          anInternalOffset = 0.00001
          anExternalOffset = -0.00001
#        else:
#          anInternalOffset = 0.
#          anExternalOffset = 0.00001
        
    aHoleInternal = self.createBox(theParameters.m_Length,
                                   anInternalWidth,
                                   theParameters.m_Height,0,0,0,theTitle + "Internal" + aLabelPostfix)
    aHoleInternalBase = self.roundBoxFrontBack(aHoleInternal, aHoleInternal.Label+"Base", theParameters.m_Height/2.-0.00001)
    aHoleInternalBase.Placement.Base.x = anInternalOffset

    aHoleExternal = self.createBox(theParameters.m_Length + 2*theParameters.m_BorderHeight,
                                   aBorderWidth,
                                   theParameters.m_Height + 2*theParameters.m_BorderHeight,0,0,0,theTitle + "External" + aLabelPostfix)
    aHoleExternalBase = self.roundBoxFrontBack(aHoleExternal,aHoleExternal.Label+"Base",theParameters.m_Height/2.-0.01)
    aHoleExternalBase.Placement.Base.x = -theParameters.m_BorderHeight
    aHoleExternalBase.Placement.Base.y = anExternalOffset
    aHoleExternalBase.Placement.Base.z = -theParameters.m_BorderHeight

    aHoleFusion = self.joinObjects([aHoleInternalBase,aHoleExternalBase],theTitle + aLabelPostfix)
   
    anOffsetY = 0
    if isFront == False:
      anOffsetY = self.m_Parameters.m_GeneralParameters.m_Width - self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth
    if not isHole:
      if isFront:
        anOffsetY = anOffsetY - 40.
      else:
        anOffsetY = anOffsetY + 40.
    anOffsetX = theParameters.m_Offset
    if theParameters.m_isCenterPanel:
      anOffsetX = (self.m_Parameters.m_GeneralParameters.m_Length - theParameters.m_Length)/2.
    anOffsetZ = self.m_Parameters.m_GeneralParameters.m_BottomHeight - theParameters.m_Height/2.
    aHoleFusion.Placement.Base.x = anOffsetX
    aHoleFusion.Placement.Base.y = anOffsetY
    aHoleFusion.Placement.Base.z = anOffsetZ
    
    if not isHole:
      return theTopBase, theBottomBase  
    aTopCut = self.cutObjects(theTopBase,aHoleFusion,"Top" + theTitle + "Cut")
    aBottomCut = self.cutObjects(theBottomBase,aHoleFusion,"Bottom" + theTitle + "Cut")
    return aTopCut, aBottomCut

  def createLeftRightPanel(self, theTopBase, theBottomBase, theTitle, theParameters, isLeft, isHole):
#    self.m_isCreate = True
#    self.m_Length = 26.
#    self.m_Height = 18.
#    self.m_isCenterPanel = False
#    self.m_Offset = 52.
#    self.m_BorderHeight = 1.5
#    self.m_isDefaultBorderWidth = True
#    self.m_BorderWidth = 1.
#    self.m_isCreateSimplePanel = True
#    self.m_BorderWidthReduce = 0.2
    if theParameters.m_isCreate==False:
      return theTopBase, theBottomBase
    aLabelPostfix = ""
    aBorderWidth = theParameters.m_BorderWidth
    if theParameters.m_isDefaultBorderWidth:
      aBorderWidth = self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth/3
    anInternalWidth = self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth
    anExternalOffset = (self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth - aBorderWidth)/2
    anInternalOffset = 0
    if isHole:
      aLabelPostfix = "Hole"
    else:
      aBorderWidth = aBorderWidth - theParameters.m_BorderWidthReduce
      anExternalOffset = anExternalOffset + theParameters.m_BorderWidthReduce/2.
      if theParameters.m_isCreateSimplePanel:
        anInternalWidth = anExternalOffset + aBorderWidth - 0.00001
        if not isLeft:
          anInternalOffset = 0.00001
          anExternalOffset = 0

    aHoleInternal = self.createBox(anInternalWidth, theParameters.m_Length,theParameters.m_Height,0,0,0,theTitle + "Internal" + aLabelPostfix)
    aHoleInternalBase = self.roundBoxLeftRight(aHoleInternal, aHoleInternal.Label+"Base", theParameters.m_Height/2.-0.00001)
    aHoleInternalBase.Placement.Base.x = anInternalOffset

    aHoleExternal = self.createBox(aBorderWidth,theParameters.m_Length + 2*theParameters.m_BorderHeight,
                                   theParameters.m_Height + 2*theParameters.m_BorderHeight,0,0,0,theTitle + "External" + aLabelPostfix)
    aHoleExternalBase = self.roundBoxLeftRight(aHoleExternal,aHoleExternal.Label+"Base",theParameters.m_Height/2.-0.01)

    aHoleExternalBase.Placement.Base.x = anExternalOffset
    aHoleExternalBase.Placement.Base.y = -theParameters.m_BorderHeight
    aHoleExternalBase.Placement.Base.z = -theParameters.m_BorderHeight

    aHoleFusion = self.joinObjects([aHoleInternalBase,aHoleExternalBase],theTitle)
    
    anOffsetX = 0
    if isLeft == False:
      anOffsetX = self.m_Parameters.m_GeneralParameters.m_Length - self.m_Parameters.m_GeneralParameters.m_VerticalBorderWidth
    if not isHole:
      if isLeft:
        anOffsetX = anOffsetX - 40.
      else:
        anOffsetX = anOffsetX + 40.

    anOffsetY = theParameters.m_Offset
    if theParameters.m_isCenterPanel:
      anOffsetY = (self.m_Parameters.m_GeneralParameters.m_Width - theParameters.m_Length)/2.
    anOffsetZ = self.m_Parameters.m_GeneralParameters.m_BottomHeight - theParameters.m_Height/2.
    aHoleFusion.Placement.Base.x = anOffsetX
    aHoleFusion.Placement.Base.y = anOffsetY
    aHoleFusion.Placement.Base.z = anOffsetZ
    if not isHole:
      return theTopBase, theBottomBase  

    aTopCut = self.cutObjects(theTopBase,aHoleFusion,"Top" + theTitle + "Cut")
    aBottomCut = self.cutObjects(theBottomBase,aHoleFusion,"Bottom" + theTitle + "Cut")

    return aTopCut, aBottomCut

  def createEar(self,theParameters,theIndx):
    aLabel = "Ear" + str(theIndx)
    aLength = theParameters.m_Length
    aWidth = theParameters.m_Width
    aHeight = theParameters.m_Height
    if theParameters.m_Base == EarParameters.FRONT_BASE or theParameters.m_Base == EarParameters.BACK_BASE:
      aWidth = theParameters.m_Height
      aHeight = theParameters.m_Width
    aEarBase = self.createBox(aLength, aWidth, aHeight, 0, 0, 0, aLabel + "Base")
 
# Macro End: D:\3dPrinter\FreeCADMacroses\CrazyHomeEnclosure.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
