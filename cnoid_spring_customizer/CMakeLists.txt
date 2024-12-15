cmake_minimum_required(VERSION 3.5.0)
project(IRSL_SpringCustomizer)

#add_compile_options(-std=c++11)
set(CMAKE_BUILD_TYPE Release)

find_package(choreonoid REQUIRED)

find_package(yaml-cpp REQUIRED)
#(YAML_CPP REQUIRED yaml-cpp)

### debug print variables
##get_cmake_property(_variableNames CACHE_VARIABLES)
#get_cmake_property(_variableNames VARIABLES)
#message("VARIABLES>>>>")
#list (SORT _variableNames)
#foreach (_variableName ${_variableNames})
#  message("${_variableName}=${${_variableName}}")
#endforeach()
#message("VARIABLES<<<<")

###########
## Build ##
###########

## Declare a C++ library
add_library(${PROJECT_NAME} SHARED
  src/SpringCustomizer.cpp
)

#set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME ${PROJECT_NAME})
set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "" SUFFIX ".so")

target_link_libraries(${PROJECT_NAME} PUBLIC
  Choreonoid::CnoidBody
  ${YAML_CPP_LIBRARIES}
)

target_include_directories(${PROJECT_NAME} PUBLIC
  ${CHOREONOID_INCLUDE_DIRS}
  ${YAML_CPP__INCLUDE_DIRS}
)

#############
## Install ##
#############
install(TARGETS ${PROJECT_NAME}
  #ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CHOREONOID_PLUGIN_DIR}/customizer
  RUNTIME DESTINATION ${CHOREONOID_PLUGIN_DIR}/customizer
  )
