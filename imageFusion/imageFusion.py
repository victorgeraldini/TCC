import os
import unittest
import vtk, qt, ctk, slicer, numpy
from slicer.ScriptedLoadableModule import *
import logging

#
# imageFusion
#

class imageFusion(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "imageFusion" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Epilepsy"]
    self.parent.dependencies = []
    self.parent.contributors = ["Victor Geraldini"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    Plugin para realizar a fusao de imagens pre-cirurgicas de CT/MRI de pacientes epilepticos.
    Plugin to merge image pre-cirurgical images of CT/MRI of patients with epilepsy.
    """
    self.parent.acknowledgementText = """
    Esse modulo foi desenvolvido como o trabalho de conclusao de curso do aluno Victor Rezende Geraldini, do curso de Informatica Biomedica, 
    da Universidade de Sao Paulo (USP) - Ribeirao Preto.
    This module was developed as the term paper of the student Victor Rezende Geraldini, in the course of Biomedical Informatics, in University
    of Sao Paulo (USP) - Ribeirao Preto.
""" # replace with organization, grant and thanks.

#
# imageFusionWidget
#

class imageFusionWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    #Instantiating widgets...

    ####### GENERAL COLLAPSIBLE BUTTON #######

    pluginButton = ctk.ctkCollapsibleButton()
    pluginButton.text = "Merge Images"
    self.layout.addWidget(pluginButton)

    #Layout within the plugin resources
    pluginLayout = qt.QFormLayout(pluginButton)

    ####### FIRST COLLAPSIBLE LAYOUT #######

    #Collapsible button to show the pipeline todo list
    pipelineListButton = ctk.ctkCollapsibleButton()
    pipelineListButton.text = "To-do list"
    pluginLayout.addWidget(pipelineListButton)

    #Layout within the todo collapsible button
    pipelineListFormLayout = qt.QFormLayout(pipelineListButton)

    #Elements to be inserted into pipelineListFormLayout
    self.element1 = qt.QCheckBox()
    self.element2 = qt.QCheckBox()
    self.element3 = qt.QCheckBox()
    self.element4 = qt.QCheckBox()
    self.element5 = qt.QCheckBox()
    self.element6 = qt.QCheckBox()
    self.element7 = qt.QCheckBox()
    self.element8 = qt.QCheckBox()
    self.element9 = qt.QCheckBox()
    self.element10 = qt.QCheckBox()

    self.element1.setEnabled(0)
    self.element2.setEnabled(0)
    self.element3.setEnabled(0)
    self.element4.setEnabled(0)
    self.element5.setEnabled(0)
    self.element6.setEnabled(0)
    self.element7.setEnabled(0)
    self.element8.setEnabled(0)
    self.element9.setEnabled(0)
    self.element10.setEnabled(0)

    pipelineListFormLayout.addRow("Lista das tarefas a serem cumpridas:", self.layout.addStretch(0))
    pipelineListFormLayout.addRow("1. Load CT image ", self.element1)
    pipelineListFormLayout.addRow("2. Mark fiducials on CT ", self.element2)
    pipelineListFormLayout.addRow("3. Load MRI image ", self.element3)
    pipelineListFormLayout.addRow("4. Mark fidicials on MRI ", self.element4)
    pipelineListFormLayout.addRow("5. Calculate Transformation Matrix ", self.element5)
    pipelineListFormLayout.addRow("6. Transform CT to adjust it to MRI", self.element6)
    pipelineListFormLayout.addRow("7. Merge images", self.element7)
    pipelineListFormLayout.addRow("8. Make Adjustments", self.element8)
    pipelineListFormLayout.addRow("9. Include 3D surface", self.element9)
    pipelineListFormLayout.addRow("10. Segment subdural electrodes", self.element10)


    ####### SECOND COLLAPSIBLE LAYOUT #######


    #Collapsible button to effectivelly show things the user has to do
    pipelineChoresButton = ctk.ctkCollapsibleButton()
    pipelineChoresButton.text = "Pipeline Chores"
    pluginLayout.addWidget(pipelineChoresButton)

    #Layout within the pipelineChoresButton
    pipelineChoresLayout = qt.QFormLayout(pipelineChoresButton)

    #Add button to add CT image
    # addCTButton = ctk.ctkCollapsibleButton()
    # addCTButton.text = "Add CT Image"
    # pipelineChoresLayout.addWidget(addCTButton)
    # CTButtonLayout = qt.QFormLayout(addCTButton)
    # CTButtonLayout.addRow("Click in 'Data' (upper-left side) button to load CT image and, then, mark three fiducials\n(upper-mid-left side) on it", self.layout.addStretch(0))
    # addCTButton = qt.QPushButton("Add CT Image")
    # addCTButton.checkable = True
    # pipelineChoresLayout.addWidget(addCTButton)
    # CTLayout = qt.QFormLayout(addCTButton)
    # CTLayout.addRow("Click in 'Data' (upper-left side) button to load CT image and, then, mark three fiducials (upper-mid-left side) on it", self.layout.addStretch(0))
	
	#Button to select CT image
    self.CtSelector = slicer.qMRMLNodeComboBox()
    self.CtSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.CtSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.CtSelector.selectNodeUponCreation = True
    self.CtSelector.addEnabled = True
    self.CtSelector.removeEnabled = True
    self.CtSelector.noneEnabled = False
    self.CtSelector.showHidden = False
    self.CtSelector.showChildNodeTypes = False
    self.CtSelector.setMRMLScene( slicer.mrmlScene )
    pipelineChoresLayout.addRow("Select CT image to be used: ", self.CtSelector)

    #Add button to add MRI image
    # addMRIButton = ctk.ctkCollapsibleButton()
    # addMRIButton.text = "Add MRI Image"
    # pipelineChoresLayout.addWidget(addMRIButton)
    # MRIButtonLayout = qt.QFormLayout(addMRIButton)
    # MRIButtonLayout.addRow("Click in 'Data' (upper-left side) button to load MRI image and, then, mark three fiducials\n(upper-mid-left side) on it", self.layout.addStretch(0))
    # addMRIButton = qt.QPushButton("Add MRI Image")
    # addMRIButton.toolTip = "Select MRI image to be used."
    # pipelineChoresLayout.addWidget(addMRIButton)
	
	#Button to select MR image
    self.MriSelector = slicer.qMRMLNodeComboBox()
    self.MriSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.MriSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.MriSelector.selectNodeUponCreation = True
    self.MriSelector.addEnabled = True
    self.MriSelector.removeEnabled = True
    self.MriSelector.noneEnabled = False
    self.MriSelector.showHidden = False
    self.MriSelector.showChildNodeTypes = False
    self.MriSelector.setMRMLScene( slicer.mrmlScene )
    pipelineChoresLayout.addRow("Select MR image to be used: ", self.MriSelector)

	#Transformation matrix type button
    self.selectMatrixText = qt.QLabel("Select the transform type: ") 
    pipelineChoresLayout.addRow(self.selectMatrixText)
	
	#Buttons
    self.typeTranslation = qt.QRadioButton()
    self.typeRigid = qt.QRadioButton()
	
    pipelineChoresLayout.addRow("Rigid", self.typeRigid)
    pipelineChoresLayout.addRow("Translation", self.typeTranslation)
	
    self.typeRigid.setChecked(1)
	
	
    #Button to calculate the transformation matrix of both images
    self.calculateTransformationMatrixButton = qt.QPushButton("Calculate Transformation Matrix")
    self.calculateTransformationMatrixButton.toolTip = "Calculate transformation matrix of both CT and MRI images. Only possible if fiducials are marked in both images."
    pipelineChoresLayout.addWidget(self.calculateTransformationMatrixButton)
    self.calculateTransformationMatrixButton.enabled = False
    #Show values of transformation
    self.hadSuccessOnTransform = qt.QLabel("Had Success on transform?")
    self.rmsValue = qt.QLabel("RMS Value:")
    pipelineChoresLayout.addRow(self.hadSuccessOnTransform)
    pipelineChoresLayout.addRow(self.rmsValue)
    #self.hadSuccessOnTransform = qt.QTextEdit();
    #pipelineChoresLayout.addRow("Had success on transform?", self.layout.addStretch(0))
    #pipelineChoresLayout.addRow(self.hadSuccessOnTransform)

    #Button to adjust CT to MRI
    self.adjustCTtoMRIButton = qt.QPushButton("Adjust CT to MRI")
    self.adjustCTtoMRIButton.toolTip = "Transform the CT and Adjust it to MRI"
    pipelineChoresLayout.addWidget(self.adjustCTtoMRIButton)

    #Instructions to merge images in a same view.
    mergeImagesButton = ctk.ctkCollapsibleButton()
    mergeImagesButton.text = "Merge images in a same view"
    pipelineChoresLayout.addWidget(mergeImagesButton)
    mergeImagesLayout = qt.QFormLayout(mergeImagesButton)
    mergeImagesLayout.addRow("On axial (red) view, click on the pin, then click on the arrow (left side). Select CT as\nforeground, and use the slider (mid-down side) to set the appropriate transparency.", self.layout.addStretch(0))


    #Choose values of adjustments
    self.sliderLR = ctk.ctkSliderWidget()
    self.sliderLR.minimum = -200
    self.sliderLR.maximum = 200
    self.sliderPA = ctk.ctkSliderWidget()
    self.sliderPA.minimum = -200
    self.sliderPA.maximum = 200
    self.sliderIS = ctk.ctkSliderWidget()
    self.sliderIS.minimum = -200
    self.sliderIS.maximum = 200

    pipelineChoresLayout.addRow("LR", self.sliderLR)
    pipelineChoresLayout.addRow("PA", self.sliderPA)
    pipelineChoresLayout.addRow("IS", self.sliderIS)

    #Button to make better adjustments
    betterAdjustmentsButton = qt.QPushButton("Make better adjustments")
    betterAdjustmentsButton.toolTip = "Apply desired adjustments to the image"
    pipelineChoresLayout.addWidget(betterAdjustmentsButton)

    #Button to segment subdural electrodes
    segmentSubduralElectrodes = qt.QPushButton("Segment subdural electrodes")
    segmentSubduralElectrodes.toolTip = ""
    pipelineChoresLayout.addWidget(segmentSubduralElectrodes)
	
	#Connections
    self.CtSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectCT)
    self.MriSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectMRI)
    self.calculateTransformationMatrixButton.connect('clicked(bool)', self.calculateTransformationMatrix)
    self.adjustCTtoMRIButton.connect('clicked(bool)', self.adjustCTtoMRI)
    betterAdjustmentsButton.connect('clicked(bool)', self.betterAdjustment)
    segmentSubduralElectrodes.connect('clicked(bool)', self.segment)
	
	
  def onSelectCT(self):	
    if self.CtSelector.currentNode():
      self.element1.setChecked(1)
      if self.element3.checked:
	    self.calculateTransformationMatrixButton.enabled = True
    else:
	  self.element1.setChecked(0)
	  self.calculateTransformationMatrixButton.enabled = False
	  
  def onSelectMRI(self):	
    if self.MriSelector.currentNode():
      self.element3.setChecked(1)
      if self.element1.checked:
	    self.calculateTransformationMatrixButton.enabled = True
    else:
	  self.element3.setChecked(0)
	  self.calculateTransformationMatrixButton.enabled = False

  def calculateTransformationMatrix(self):
    logic = imageFusionLogic()
    type = None
    isRigid = self.typeRigid.checked

    if isRigid:
	  type = "Rigid"
    else:
      type = "Translation"	
	
    print("Calculate Transformation Matrix")
    logic.doTransformationMatrix(type, self.element5)
	
    if self.element5.enabled:
      self.adjustCTtoMRIButton.enabled = True
      

  def adjustCTtoMRI(self):
    logic = imageFusionLogic()
    print("Adjust CT to MRI")
    logic.doAdjustment(self.CtSelector.currentNode())

  def betterAdjustment(self):
    logic = imageFusionLogic()
    print("Doing better adjustment")
    logic.doBetterAdjustment(self.sliderLR.value, self.sliderPA.value, self.sliderIS.value)

  def segment(self):
    logic = imageFusionLogic()
    print("Segmenting")
    logic.doSegment()

	

class imageFusionLogic:
  import slicer
  import math
  def __init__(self):
    pass
	
  #Vai guardar a matriz de transformacao
  transformSave = slicer.vtkMRMLTransformNode()
  
  def doTransformationMatrix(self, type, element, transform = transformSave):
    markups = slicer.modules.markups.logic()
    fidID = markups.GetActiveListID()
    fidNode = slicer.mrmlScene.GetNodeByID(fidID)
	
    print(fidID)
	
    node1 = slicer.vtkMRMLMarkupsFiducialNode()
    node2 = slicer.vtkMRMLMarkupsFiducialNode()
    slicer.mrmlScene.AddNode(node1)
    slicer.mrmlScene.AddNode(node2)
	
    fiducial1 = [0,0,0]
    fiducial2 = [0,0,0]
    fiducial3 = [0,0,0]
    fiducial4 = [0,0,0]
    fiducial5 = [0,0,0]
    fiducial6 = [0,0,0]
    fidNode.GetNthFiducialPosition(0, fiducial1)
    fidNode.GetNthFiducialPosition(1, fiducial2)
    fidNode.GetNthFiducialPosition(2, fiducial3)
    fidNode.GetNthFiducialPosition(3, fiducial4)
    fidNode.GetNthFiducialPosition(4, fiducial5)
    fidNode.GetNthFiducialPosition(5, fiducial6)
	
    node1.AddFiducialFromArray(fiducial1)
    node1.AddFiducialFromArray(fiducial2)
    node1.AddFiducialFromArray(fiducial3)
    node2.AddFiducialFromArray(fiducial4)
    node2.AddFiducialFromArray(fiducial5)
    node2.AddFiducialFromArray(fiducial6)
	
    print("PRIMEIRO NODO")
    print(node1)
    print("SEGUNDO NODO")
    print(node2)
	
	
    print("Doing transformation matrix")
	
	
	#Create transform node
    #transformSave = slicer.vtkMRMLTransformNode()
	#Add node to scene
    slicer.mrmlScene.AddNode(transform)
	
	
	
	
    parameters = {}
    parameters["fixedLandmarks"] = node2.GetID()
    parameters["movingLandmarks"] = node1.GetID()
    parameters["saveTransform"] = transform.GetID()
    parameters["transformType"] = type
    fiducialRegistration = slicer.modules.fiducialregistration
    slicer.cli.run(fiducialRegistration, None, parameters)

	
    print(transform)
    print("TIPO DA TRANSFORMADA:")
    print(type)
	
    element.setChecked(1)
	
    # slicer.mrmlScene.AddNode(transform)
    # matrix = vtk.vtkMatrix4x4()
    # auxMatrix = []
    # transform.GetMatrixTransformFromParent(matrix)
    # rms = 0
    # for x in range(0,4):
      # for y in range(0,4):
        # auxMatrix.append(matrix.GetElement(x,y))
        # print(matrix.GetElement(x,y))
	
    # rms = numpy.sqrt(numpy.mean(numpy.square(auxMatrix)))
    # print("RMS")
    # print(rms)
    # print(auxMatrix)
    # print(matrix)
	

  def doAdjustment(self, ctImage, transform = transformSave):
    print("Adjusting CT to MRI!")
    
    ctImage.SetAndObserveTransformNodeID(transform.GetID())
    slicer.app.processEvents()
	
	
  def doBetterAdjustment(self, sliderLR, sliderPA, sliderIS, transform = transformSave):
    print("Doing better adjustments")
	
	
    slicer.mrmlScene.AddNode(transform)
	
    print("Valores dos sliders:")
    print(sliderLR)
    print(sliderPA)
    print(sliderIS)
    matrix = vtk.vtkMatrix4x4()
    transform.GetMatrixTransformFromParent(matrix)
    print("Matriz antes")
    print(matrix)
    
    matrix.SetElement(0,3, sliderLR)
    matrix.SetElement(1,3, sliderPA)
    matrix.SetElement(2,3, sliderIS)
    transform.SetMatrixTransformToParent(matrix)
	
    print("Matriz depois")
    print(matrix)

    slicer.app.processEvents()
	

    # slicer.mrmlScene.AddNode(transform)
	
    # transformable = slicer.modules.transforms
    # parameters = {}
    # parameters["Active Transform"] = transform.GetID()
    # parameters["Translation"] = [10, 20, 30]
	
    # slicer.cli.run(transformable, None, parameters)
	
  def doSegment(self):
    print("Segmenting subdural electrodes")
	
	
	
	
	
	

    #Modulos do slicer que devo usar:
    #1 Fiducial Registration (fazer transformada), https://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Modules/FiducialRegistration
    #2 Transforms, https://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Modules/Transforms
    #3 Editor, https://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Modules/Editor


#     # Instantiate and connect widgets ...

#     #
#     # Parameters Area
#     #
#     parametersCollapsibleButton = ctk.ctkCollapsibleButton()
#     parametersCollapsibleButton.text = "Parameters"
#     self.layout.addWidget(parametersCollapsibleButton)

#     # Layout within the dummy collapsible button
#     parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

#     #
#     # input volume selector
#     #
#     self.inputSelector = slicer.qMRMLNodeComboBox()
#     self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
#     self.inputSelector.selectNodeUponCreation = True
#     self.inputSelector.addEnabled = False
#     self.inputSelector.removeEnabled = False
#     self.inputSelector.noneEnabled = False
#     self.inputSelector.showHidden = False
#     self.inputSelector.showChildNodeTypes = False
#     self.inputSelector.setMRMLScene( slicer.mrmlScene )
#     self.inputSelector.setToolTip( "Pick the input to the algorithm." )
#     parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

#     #
#     # output volume selector
#     #
#     self.outputSelector = slicer.qMRMLNodeComboBox()
#     self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
#     self.outputSelector.selectNodeUponCreation = True
#     self.outputSelector.addEnabled = True
#     self.outputSelector.removeEnabled = True
#     self.outputSelector.noneEnabled = True
#     self.outputSelector.showHidden = False
#     self.outputSelector.showChildNodeTypes = False
#     self.outputSelector.setMRMLScene( slicer.mrmlScene )
#     self.outputSelector.setToolTip( "Pick the output to the algorithm." )
#     parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

#     #
#     # threshold value
#     #
#     self.imageThresholdSliderWidget = ctk.ctkSliderWidget()
#     self.imageThresholdSliderWidget.singleStep = 0.1
#     self.imageThresholdSliderWidget.minimum = -100
#     self.imageThresholdSliderWidget.maximum = 100
#     self.imageThresholdSliderWidget.value = 0.5
#     self.imageThresholdSliderWidget.setToolTip("Set threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
#     parametersFormLayout.addRow("Image threshold", self.imageThresholdSliderWidget)

#     #
#     # check box to trigger taking screen shots for later use in tutorials
#     #
#     self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
#     self.enableScreenshotsFlagCheckBox.checked = 0
#     self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
#     parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

#     #
#     # Apply Button
#     #
#     self.applyButton = qt.QPushButton("Apply")
#     self.applyButton.toolTip = "Run the algorithm."
#     self.applyButton.enabled = False
#     parametersFormLayout.addRow(self.applyButton)

#     # connections
#     self.applyButton.connect('clicked(bool)', self.onApplyButton)
#     self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
#     self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

#     # Add vertical spacer
#     self.layout.addStretch(1)

#     # Refresh Apply button state
#     self.onSelect()

#   def cleanup(self):
#     pass

#   def onSelect(self):
#     self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

#   def onApplyButton(self):
#     logic = imageFusionLogic()
#     enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
#     imageThreshold = self.imageThresholdSliderWidget.value
#     logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), imageThreshold, enableScreenshotsFlag)

# #
# # imageFusionLogic
# #

# class imageFusionLogic(ScriptedLoadableModuleLogic):
#   """This class should implement all the actual
#   computation done by your module.  The interface
#   should be such that other python code can import
#   this class and make use of the functionality without
#   requiring an instance of the Widget.
#   Uses ScriptedLoadableModuleLogic base class, available at:
#   https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
#   """

#   def hasImageData(self,volumeNode):
#     """This is an example logic method that
#     returns true if the passed in volume
#     node has valid image data
#     """
#     if not volumeNode:
#       logging.debug('hasImageData failed: no volume node')
#       return False
#     if volumeNode.GetImageData() == None:
#       logging.debug('hasImageData failed: no image data in volume node')
#       return False
#     return True

#   def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
#     """Validates if the output is not the same as input
#     """
#     if not inputVolumeNode:
#       logging.debug('isValidInputOutputData failed: no input volume node defined')
#       return False
#     if not outputVolumeNode:
#       logging.debug('isValidInputOutputData failed: no output volume node defined')
#       return False
#     if inputVolumeNode.GetID()==outputVolumeNode.GetID():
#       logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
#       return False
#     return True

#   def takeScreenshot(self,name,description,type=-1):
#     # show the message even if not taking a screen shot
#     slicer.util.delayDisplay('Take screenshot: '+description+'.\nResult is available in the Annotations module.', 3000)

#     lm = slicer.app.layoutManager()
#     # switch on the type to get the requested window
#     widget = 0
#     if type == slicer.qMRMLScreenShotDialog.FullLayout:
#       # full layout
#       widget = lm.viewport()
#     elif type == slicer.qMRMLScreenShotDialog.ThreeD:
#       # just the 3D window
#       widget = lm.threeDWidget(0).threeDView()
#     elif type == slicer.qMRMLScreenShotDialog.Red:
#       # red slice window
#       widget = lm.sliceWidget("Red")
#     elif type == slicer.qMRMLScreenShotDialog.Yellow:
#       # yellow slice window
#       widget = lm.sliceWidget("Yellow")
#     elif type == slicer.qMRMLScreenShotDialog.Green:
#       # green slice window
#       widget = lm.sliceWidget("Green")
#     else:
#       # default to using the full window
#       widget = slicer.util.mainWindow()
#       # reset the type so that the node is set correctly
#       type = slicer.qMRMLScreenShotDialog.FullLayout

#     # grab and convert to vtk image data
#     qpixMap = qt.QPixmap().grabWidget(widget)
#     qimage = qpixMap.toImage()
#     imageData = vtk.vtkImageData()
#     slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

#     annotationLogic = slicer.modules.annotations.logic()
#     annotationLogic.CreateSnapShot(name, description, type, 1, imageData)

#   def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
#     """
#     Run the actual algorithm
#     """

#     if not self.isValidInputOutputData(inputVolume, outputVolume):
#       slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
#       return False

#     logging.info('Processing started')

#     # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
#     cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
#     cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

#     # Capture screenshot
#     if enableScreenshots:
#       self.takeScreenshot('imageFusionTest-Start','MyScreenshot',-1)

#     logging.info('Processing completed')

#     return True


# class imageFusionTest(ScriptedLoadableModuleTest):
#   """
#   This is the test case for your scripted module.
#   Uses ScriptedLoadableModuleTest base class, available at:
#   https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
#   """

#   def setUp(self):
#     """ Do whatever is needed to reset the state - typically a scene clear will be enough.
#     """
#     slicer.mrmlScene.Clear(0)

#   def runTest(self):
#     """Run as few or as many tests as needed here.
#     """
#     self.setUp()
#     self.test_imageFusion1()

#   def test_imageFusion1(self):
#     """ Ideally you should have several levels of tests.  At the lowest level
#     tests should exercise the functionality of the logic with different inputs
#     (both valid and invalid).  At higher levels your tests should emulate the
#     way the user would interact with your code and confirm that it still works
#     the way you intended.
#     One of the most important features of the tests is that it should alert other
#     developers when their changes will have an impact on the behavior of your
#     module.  For example, if a developer removes a feature that you depend on,
#     your test should break so they know that the feature is needed.
#     """

#     self.delayDisplay("Starting the test")
#     #
#     # first, get some data
#     #
#     import urllib
#     downloads = (
#         ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
#         )

#     for url,name,loader in downloads:
#       filePath = slicer.app.temporaryPath + '/' + name
#       if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
#         logging.info('Requesting download %s from %s...\n' % (name, url))
#         urllib.urlretrieve(url, filePath)
#       if loader:
#         logging.info('Loading %s...' % (name,))
#         loader(filePath)
#     self.delayDisplay('Finished with download and loading')

#     volumeNode = slicer.util.getNode(pattern="FA")
#     logic = imageFusionLogic()
#     self.assertTrue( logic.hasImageData(volumeNode) )
#     self.delayDisplay('Test passed!')
