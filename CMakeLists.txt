cmake_minimum_required(VERSION 2.8.9)

project(Epilepsy)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/Epilepsy")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Victor Geraldini (Universidade de São Paulo)")
set(EXTENSION_DESCRIPTION "Módulo para o trabalho de conclusão do curso de informática biomédica do aluno Victor Geraldini")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/Epilepsy.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/Epilepsy/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(imageFusion)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
