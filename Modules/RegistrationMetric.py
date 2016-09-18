import os
import unittest
import qt, vtk
from __main__ import ctk, slicer
import DataProbeLib

#
# RegistrationMetric
#

class RegistrationMetric:
  def __init__(self, parent):
    parent.title = "RegistrationMetric"
    parent.categories = ["Epilepsy"]
    parent.dependencies = []
    parent.contributors = ["Veronique Ferry and Fabricio Simozo (CSIM)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """ This is a module for 3D Slicer to assess the registration of pre and post-surgery image volumes. """
    parent.acknowledgementText = """ This module was developped by Veronique Ferry and was partly funded by 'Bourse Alsace Mobilite'. """ # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created. Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['RegistrationMetric'] = self.runTest

  def runTest(self):
    tester = RegistrationMetricTest()
    tester.runTest()

#
# qRegistrationMetricWidget
#

class RegistrationMetricWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()



  def setup(self):
    # Instantiate and connect widgets ...

    #
    # Collapsible Button to paint pixels
    #
    pixelPaintingCollapsibleButton = ctk.ctkCollapsibleButton()
    pixelPaintingCollapsibleButton.text = "Pixel Painting"
    self.layout.addWidget(pixelPaintingCollapsibleButton)

    # Layout within the collapsible button
    pixelPaintingFormLayout = qt.QFormLayout(pixelPaintingCollapsibleButton)

    #
    # Check Box to enable pixel painting
    #
    self.enablePixelPaintingCheckBox = qt.QCheckBox()
    self.enablePixelPaintingCheckBox.checked = 0
    self.enablePixelPaintingCheckBox.setToolTip("If checked, paint selected pixel by mouse hovering and pressing 'p' key.")
    pixelPaintingFormLayout.addRow("Enable Pixel Painting", self.enablePixelPaintingCheckBox)

    #
    # Spin Box to choose intensity value of pixels to paint
    #
    self.paintedPixelValueEdit = qt.QSpinBox()
    self.paintedPixelValueEdit.setMinimum(5000)
    self.paintedPixelValueEdit.setMaximum(15000)
    self.paintedPixelValueEdit.setSingleStep(50)
    self.paintedPixelValueEdit.setValue(7500)
    pixelPaintingFormLayout.addRow("Choose intensity value of pixels to paint:", self.paintedPixelValueEdit)

    self.spaceAfterPaint = qt.QLabel(" ")
    pixelPaintingFormLayout.addRow(self.spaceAfterPaint)

    #
    # Collapsible Button to compute metric distance
    #
    metricDistanceCollapsibleButton = ctk.ctkCollapsibleButton()
    metricDistanceCollapsibleButton.text = "Compute Metric Distance between markers"
    self.layout.addWidget(metricDistanceCollapsibleButton)

    # Layout within the collapsible button
    metricDistanceFormLayout = qt.QFormLayout(metricDistanceCollapsibleButton)


    #
    # Fixed Image with Markers Selector 1
    #
    self.resultSelector1 = slicer.qMRMLNodeComboBox()
    self.resultSelector1.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.resultSelector1.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.resultSelector1.selectNodeUponCreation = True
    self.resultSelector1.addEnabled = True
    self.resultSelector1.removeEnabled = True
    self.resultSelector1.noneEnabled = False
    self.resultSelector1.showHidden = False
    self.resultSelector1.showChildNodeTypes = False
    self.resultSelector1.setMRMLScene( slicer.mrmlScene )
    self.resultSelector1.setToolTip( "Pick fixed image with markers" )
    metricDistanceFormLayout.addRow("Fixed Image with markers: ", self.resultSelector1)

    #
    # Registered Image Volume Selector 2
    #
    self.resultSelector2 = slicer.qMRMLNodeComboBox()
    self.resultSelector2.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.resultSelector2.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.resultSelector2.selectNodeUponCreation = True
    self.resultSelector2.addEnabled = True
    self.resultSelector2.removeEnabled = True
    self.resultSelector2.noneEnabled = False
    self.resultSelector2.showHidden = False
    self.resultSelector2.showChildNodeTypes = False
    self.resultSelector2.setMRMLScene( slicer.mrmlScene )
    self.resultSelector2.setToolTip( "Pick subtracted image from registered images" )
    metricDistanceFormLayout.addRow("Subtracted Image of registered images with and without markers: ", self.resultSelector2)

    #
    # Apply Button
    #
    self.spaceBeforeApply = qt.QLabel(" ")
    metricDistanceFormLayout.addRow(self.spaceBeforeApply)

    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    metricDistanceFormLayout.addRow(self.applyButton)

    #
    # CrosshairNode listenner
    #
    self.CrosshairNode = None
    self.CrosshairNodeObserverTag = None

    # Observe the crosshair node to get the current cursor position
    self.CrosshairNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLCrosshairNode')
    if self.CrosshairNode:
      self.CrosshairNodeObserverTag = self.CrosshairNode.AddObserver(slicer.vtkMRMLCrosshairNode.CursorPositionModifiedEvent, self.doNothing)

    #
    # Observe shortcut - press 'p' to paint where mouse points
    #
    shortcut = qt.QShortcut(slicer.util.mainWindow())
    shortcut.setKey( qt.QKeySequence('p') )
    shortcut.connect( 'activated()', self.processEvent )

    #
    # connections
    #
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.resultSelector1.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.resultSelector2.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)


    # Add vertical spacer
    self.layout.addStretch(1)


  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.resultSelector1.currentNode() and self.resultSelector2.currentNode()

  def onApplyButton(self):
    logic = RegistrationMetricLogic()
    print("Run the algorithm")

    logic.run(self.resultSelector1.currentNode(), self.resultSelector2.currentNode())

    #
    # Function to paint pixels where mouse points
    #
  def paintPixel(self,volumeNode,ijk):
    if self.enablePixelPaintingCheckBox.checked == True:
      if volumeNode:
        imageData = volumeNode.GetImageData()
        if imageData and imageData.GetScalarSize() > 1:
          imageData.SetScalarComponentFromDouble(ijk[0], ijk[1], ijk[2], 0, self.paintedPixelValueEdit.value)
        else:
           print("No Image")
      else:
         print("No Volume")

###

  def __del__(self):
    self.removeObservers()


  def removeObservers(self):
    # remove observers and reset
    if self.CrosshairNode and self.CrosshairNodeObserverTag:
      self.CrosshairNode.RemoveObserver(self.CrosshairNodeObserverTag)
    self.CrosshairNodeObserverTag = None

  def doNothing(self, observee, event):
    #do nothing -> the crosshair node is only there to know the coordinates of the pixel where the mouse points
    xyz = [0.0,0.0,0.0]

  def processEvent(self):
    """
    handle events from the render window interactor
    """
    xyz = [0.0,0.0,0.0]

    sliceNode = None
    if self.CrosshairNode:
      sliceNode = self.CrosshairNode.GetCursorPositionXYZ(xyz)

    sliceLogic = None
    if sliceNode:
      appLogic = slicer.app.applicationLogic()
      if appLogic:
        sliceLogic = appLogic.GetSliceLogic(sliceNode)

    volumeLogic = sliceLogic.GetBackgroundLayer()
    volumeNode = volumeLogic.GetVolumeNode()

    if volumeNode:
        xyToIJK = volumeLogic.GetXYToIJKTransform()
        ijkFloat = xyToIJK.TransformDoublePoint(xyz)
        ijk = []
        for element in ijkFloat:
          try:
            index = int(round(element))
          except ValueError:
            index = 0
          ijk.append(index)
        self.paintPixel(volumeNode,ijk)


#
# RegistrationMetricLogic
#
class RegistrationMetricLogic:
  """This class should implement all the actual
computation done by your module. The interface
should be such that other python code can import
this class and make use of the functionality without
requiring an instance of the Widget
"""
  import slicer
  import math
  def __init__(self):
    pass


  def run(self, resultSelector1, resultSelector2):

    if resultSelector1 and resultSelector2:
        imageDataFixed = resultSelector1.GetImageData()
        imageDataSubtracted = resultSelector2.GetImageData()
        if imageDataFixed and imageDataSubtracted:
            dimFixed = imageDataFixed.GetDimensions()
            dimSubtracted = imageDataFixed.GetDimensions()
            max= imageDataSubtracted.GetScalarComponentAsDouble(0, 0, 0, 0)
            indxFixed = []
            indyFixed = []
            indzFixed = []
            indxSubtracted = []
            indySubtracted = []
            indzSubtracted = []
            maxSubtracted = []

            # Nested loops over pixels in fixed image to find markers coordinates
            for z in range ( 0, dimFixed[2] ):
              for y in range ( 0, dimFixed[1] ):
                for x in range ( 0, dimFixed[0] ):
                  if imageDataFixed.GetScalarComponentAsDouble(x, y, z, 0) >= 5000: # 5000 is the minimum intensity value for markers and is above pixel values in image
                    indxFixed.append(x)
                    indyFixed.append(y)
                    indzFixed.append(z)
            markersNumber = len(indxFixed)
            pixelsGroups = []
            resultingMarkers = []

            # Creation of a list containing the coordinates of the bright pixels in subtracted image ordered by groups of pixels corresponding to the original markers
            for i in range (0, markersNumber):
              pixelsGroups.append([])

            # Nested loops over pixels in subtracted image to find markers coordinates
            for z in range ( 0, dimSubtracted[2] ):
              for y in range ( 0, dimSubtracted[1] ):
                for x in range ( 0, dimSubtracted[0] ):
                  if imageDataSubtracted.GetScalarComponentAsDouble(x, y, z, 0) >= 10:
                    max = imageDataSubtracted.GetScalarComponentAsDouble(x, y, z, 0)
                    indxSubtracted.append(x)
                    indySubtracted.append(y)
                    indzSubtracted.append(z)
                    maxSubtracted.append(max)
            brightPixelsNumber = len(indxSubtracted)

            # Compute distances between each point found in the Subtracted Image and markers from Fixed Image
            for i in range (0, brightPixelsNumber):
              distMin = math.sqrt((indxSubtracted[i]-indxFixed[0])**2 + (indySubtracted[i]-indyFixed[0])**2 + (indzSubtracted[i]-indzFixed[0])**2)
              indMin = 0
              for j in range (0, markersNumber):
                if math.sqrt((indxSubtracted[i]-indxFixed[j])**2 + (indySubtracted[i]-indyFixed[j])**2 + (indzSubtracted[i]-indzFixed[j])**2) < distMin:
                  distMin = math.sqrt((indxSubtracted[i]-indxFixed[j])**2 + (indySubtracted[i]-indyFixed[j])**2 + (indzSubtracted[i]-indzFixed[j])**2)
                  indMin = j

              pixelsGroups[indMin].append((indxSubtracted[i], indySubtracted[i], indzSubtracted[i], maxSubtracted[i]))

            # Do weighted mean for each pixel group to find coordinates of resulting marker post-registration
            for i in range (0, markersNumber):
              sumx = 0
              sumy = 0
              sumz = 0
              sumDiv = 0
              for j in range (0, len(pixelsGroups[i])):
                sumx = sumx + pixelsGroups[i][j][3]*pixelsGroups[i][j][0]
                sumy = sumy + pixelsGroups[i][j][3]*pixelsGroups[i][j][1]
                sumz = sumz + pixelsGroups[i][j][3]*pixelsGroups[i][j][2]
                sumDiv = sumDiv + pixelsGroups[i][j][3]
              if sumDiv != 0:
                x = sumx/sumDiv
                y = sumy/sumDiv
                z = sumz/sumDiv
              else:
                x = 0
                y = 0
                z = 0
                print("No pixels corresponding to marker ", i+1, " of coordinates: x = ", indxFixed[i], ", y = ", indyFixed[i], ", z = ", indzFixed[i])
              resultingMarkers.append((x, y, z))

            # Compute distance original marker and resulting marker
            distanceBetweenMarkers = []
            for i in range (0, markersNumber):
              if resultingMarkers[i][0]==0 and resultingMarkers[i][1]==0 and resultingMarkers[i][2]==0:
                dist = "None"
              else:
                dist = math.sqrt((resultingMarkers[i][0]-indxFixed[i])**2 + (resultingMarkers[i][1]-indyFixed[i])**2 + (resultingMarkers[i][2]-indzFixed[i])**2)
              distanceBetweenMarkers.append(dist)


            qt.QMessageBox.warning(slicer.util.mainWindow(), "Finished!", "The algorithm was run successfully!")

            # Print coordinates of markers in fixed image and metric distance with corresponding markers in subtracted image
            print("X markers coordinates in Fixed Image:", indxFixed)
            print("Y markers coordinates in Fixed Image:", indyFixed)
            print("Z markers coordinates in Fixed Image:", indzFixed)
            print("distances between original and resulting markers:", distanceBetweenMarkers)

        else:
          print("No Image")
    else:
      print("No Volume")

    return True



