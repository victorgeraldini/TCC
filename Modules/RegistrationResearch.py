import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# RegistrationResearch
#

class RegistrationResearch:
  def __init__(self, parent):
    parent.title = "RegistrationResearch"
    parent.categories = ["Epilepsy"]
    parent.dependencies = []
    parent.contributors = ["Emylin Sousa (SPL)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """ This is a module for 3D Slicer to provide rigid and nonrigid registration identifying ressecting regions in epilepsy, both from pre to post-surgical MRI and from post to pre-surgicclass RegistrationMetric: """
    parent.acknowledgementText = """
This module was developed by Emylin Sousa and was funded by Brazil Scientific Mobility Program.
""" # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created. Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['RegistrationResearch'] = self.runTest

  def runTest(self):
    tester = RegistrationResearchTest()
    tester.runTest()

#
# qRegistrationResearchWidget
#

class RegistrationResearchWidget:
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
    # Reload and Test area
    # TODO: delete before deliver ----- from here -----

    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "RegistrationResearch Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    reloadFormLayout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    # ----- to here -----

    #
    # inputImages Area
    #
    inputImagesCollapsibleButton = ctk.ctkCollapsibleButton()
    inputImagesCollapsibleButton.text = "Input Images"
    self.layout.addWidget(inputImagesCollapsibleButton)

    # Layout within the collapsible button
    inputImagesFormLayout = qt.QFormLayout(inputImagesCollapsibleButton)

    #
    # Fixed Image Volume Selector
    #
    self.fixedSelector = slicer.qMRMLNodeComboBox()
    self.fixedSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.fixedSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.fixedSelector.selectNodeUponCreation = True
    self.fixedSelector.addEnabled = True
    self.fixedSelector.removeEnabled = True
    self.fixedSelector.noneEnabled = False
    self.fixedSelector.showHidden = False
    self.fixedSelector.showChildNodeTypes = False
    self.fixedSelector.setMRMLScene( slicer.mrmlScene )
    self.fixedSelector.setToolTip( "Pick the fixed image to the algorithm." )
    inputImagesFormLayout.addRow("Fixed Image Selector: ", self.fixedSelector)

    #
    # Moving Image Volume Selector
    #
    self.movingSelector = slicer.qMRMLNodeComboBox()
    self.movingSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.movingSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.movingSelector.selectNodeUponCreation = True
    self.movingSelector.addEnabled = True
    self.movingSelector.removeEnabled = True
    self.movingSelector.noneEnabled = False
    self.movingSelector.showHidden = False
    self.movingSelector.showChildNodeTypes = False
    self.movingSelector.setMRMLScene( slicer.mrmlScene )
    self.movingSelector.setToolTip( "Pick the moving image to the algorithm." )
    inputImagesFormLayout.addRow("Moving Image Selector: ", self.movingSelector)

    #
    # Result Image Volume Selector
    #
    self.resultSelector = slicer.qMRMLNodeComboBox()
    self.resultSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.resultSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.resultSelector.selectNodeUponCreation = True
    self.resultSelector.addEnabled = True
    self.resultSelector.removeEnabled = True
    self.resultSelector.noneEnabled = False
    self.resultSelector.showHidden = False
    self.resultSelector.showChildNodeTypes = False
    self.resultSelector.setMRMLScene( slicer.mrmlScene )
    self.resultSelector.setToolTip( "Pick the result image to the algorithm." )
    inputImagesFormLayout.addRow("Result Image Selector: ", self.resultSelector)
	
	#
    # Quadratic Difference Image Volume Selector
    #
    self.quadraticDifferenceSelector = slicer.qMRMLNodeComboBox()
    self.quadraticDifferenceSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.quadraticDifferenceSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.quadraticDifferenceSelector.selectNodeUponCreation = True
    self.quadraticDifferenceSelector.addEnabled = True
    self.quadraticDifferenceSelector.removeEnabled = True
    self.quadraticDifferenceSelector.noneEnabled = False
    self.quadraticDifferenceSelector.showHidden = False
    self.quadraticDifferenceSelector.showChildNodeTypes = False
    self.quadraticDifferenceSelector.setMRMLScene( slicer.mrmlScene )
    self.quadraticDifferenceSelector.setToolTip( "Pick the quadratic difference image to the algorithm." )
    inputImagesFormLayout.addRow("Quadratic Difference Image Selector: ", self.quadraticDifferenceSelector)


    #
    # Image Registration Type
    #

    registrationTypeCollapsibleButton = ctk.ctkCollapsibleButton()
    registrationTypeCollapsibleButton.text = "Options"
    self.layout.addWidget(registrationTypeCollapsibleButton)

    # Layout within the collapsible button
    registrationTypeFormLayout = qt.QFormLayout(registrationTypeCollapsibleButton)

    #
    # Image Registration Type Selector 
    #
	
    self.selectRegistration = qt.QLabel("Select Registration Type")
    self.selectRegistration.setMargin(7)
    registrationTypeFormLayout.addRow(self.selectRegistration)

    self.rigidRegistration = qt.QRadioButton()
    self.rigidAndNonRigidRegistration = qt.QRadioButton()

    registrationTypeFormLayout.addRow("Rigid Registration only", self.rigidRegistration)
    registrationTypeFormLayout.addRow("Rigid Registration followed by Non-Rigid Registration", self.rigidAndNonRigidRegistration)

    self.rigidRegistration.setChecked(1)
	
    #
    # check box to select quadratic difference
    #
    self.outputLabel = qt.QLabel("Output")
    self.outputLabel.setMargin(7)
    registrationTypeFormLayout.addRow(self.outputLabel)
	
    self.enableQuadraticDifferenceCheckBox = qt.QCheckBox()
    self.enableQuadraticDifferenceCheckBox.checked = 0
    self.enableQuadraticDifferenceCheckBox.setToolTip("If checked, calculate quadratic difference from fixed and result images.")
    registrationTypeFormLayout.addRow("Enable Quadratic Difference", self.enableQuadraticDifferenceCheckBox)

    #
    # Apply Button
    #
	
    self.spaceBeforeApply = qt.QLabel(" ")
    registrationTypeFormLayout.addRow(self.spaceBeforeApply)
	
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    registrationTypeFormLayout.addRow(self.applyButton)
	
	# TODO: create a progress bar

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.fixedSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.movingSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.resultSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.quadraticDifferenceSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.fixedSelector.currentNode() and self.movingSelector.currentNode() and self.resultSelector.currentNode()

  def onApplyButton(self):
    logic = RegistrationResearchLogic()
    rigidButtonChecked = self.rigidRegistration.isChecked()
    quadraticDifferenceFlag = self.enableQuadraticDifferenceCheckBox.checked
    print("Run the algorithm")
    print(rigidButtonChecked)
    print(quadraticDifferenceFlag)

    logic.run(self.fixedSelector.currentNode(), self.movingSelector.currentNode(), self.resultSelector.currentNode(), self.quadraticDifferenceSelector.currentNode(), rigidButtonChecked, quadraticDifferenceFlag)

    # TODO: delete before deliver ----- from here -----

  def onReload(self,moduleName="RegistrationResearch"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent().parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)

    # delete the old widget instance
    if hasattr(globals()['slicer'].modules, widgetName):
      getattr(globals()['slicer'].modules, widgetName).cleanup()

    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()
    setattr(globals()['slicer'].modules, widgetName, globals()[widgetName.lower()])

  def onReloadAndTest(self,moduleName="RegistrationResearch"):
    try:
      self.onReload()
      evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
      tester = eval(evalString)
      tester.runTest()
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(), 
          "Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")

    # ----- to here -----


#
# RegistrationResearchLogic
#

class RegistrationResearchLogic:
  """This class should implement all the actual
computation done by your module. The interface
should be such that other python code can import
this class and make use of the functionality without
requiring an instance of the Widget
"""
  import slicer
  def __init__(self):
    pass

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that
returns true if the passed in volume
node has valid image data
"""
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True


  def run(self, fixedSelector, movingSelector, resultSelector, quadraticDifferenceSelector, rigidButtonChecked, quadraticDifferenceFlag):

    # first option selected
    if rigidButtonChecked == True:
      cliNode = self.doRigid(fixedSelector, movingSelector, resultSelector)

    # second option selected
    else:
      cliNode4 = self.doBrainsFit(fixedSelector, movingSelector, resultSelector)
    	
    # output option
    if quadraticDifferenceFlag == True:
      cliNode2 = self.doSubtractVolumes(fixedSelector, resultSelector, quadraticDifferenceSelector)
      cliNode3 = self.doMultiplyVolumes(quadraticDifferenceSelector)      

    return True
	
  #
  # do rigid registration
  #
  def doRigid(self, fixedNode, movingNode, resultNode):
    print('First Option Checked')
    parameters = {}
    parameters["FixedImageFileName"] = fixedNode.GetID()
    parameters["MovingImageFileName"] = movingNode.GetID()
    parameters["ResampledImageFileName"] = resultNode.GetID()
    rigidMaker = slicer.modules.rigidregistration
    return (slicer.cli.run(rigidMaker, None, parameters))
	
  #
  # General Registration (BRAINS Fit)
  #
  def doBrainsFit(self, fixedNode, movingNode, resultNode):
    print('Second Option Checked')
    parameters = {}
    parameters["fixedVolume"] = fixedNode.GetID()
    parameters["movingVolume"] = movingNode.GetID()
    parameters["outputVolume"] = resultNode.GetID()
    parameters["useRigid"] = True
    parameters["useBSpline"] = True
    brainsFitMaker = slicer.modules.brainsfit
    return (slicer.cli.run(brainsFitMaker, None, parameters))

  #
  # subtract scalar volumes
  #
  def doSubtractVolumes(self, fixedNode, resultNode, quadraticDifferenceNode):
    print('Quadratic Difference Flag Checked')
    parameters = {}
    parameters["inputVolume1"] = fixedNode.GetID()
    parameters["inputVolume2"] = resultNode.GetID()
    parameters["outputVolume"] = quadraticDifferenceNode.GetID()
    subtractVolumeMaker = slicer.modules.subtractscalarvolumes
    return (slicer.cli.run(subtractVolumeMaker, None, parameters))

  #
  # multiply scalar volumes
  #
  def doMultiplyVolumes(self, quadraticDifferenceNode):
    print('Multiply Volume Function')
    parameters = {}
    parameters["inputVolume1"] = quadraticDifferenceNode.GetID()
    parameters["inputVolume2"] = quadraticDifferenceNode.GetID()
    parameters["outputVolume"] = quadraticDifferenceNode.GetID()
    multiplyVolumeMaker = slicer.modules.multiplyscalarvolumes
    return (slicer.cli.run(multiplyVolumeMaker, None, parameters))











 



    





