cmake_minimum_required(VERSION 2.8.12)
project(iris_distro)

include(ExternalProject)

if(APPLE AND POLICY CMP0042)
  # MACOSX_RPATH is enabled by default.
  cmake_policy(SET CMP0042 NEW)
endif()

# Set the default build type.
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING
    "Choose the type of build; options are Debug Release RelWithDebInfo MinSizeRel."
    FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
    Debug Release RelWithDebInfo MinSizeRel)
endif()

# Set the default installation prefix.
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/install" CACHE STRING
    "TODO" FORCE)
endif()

option(BUILD_TESTING "Build the testing tree." ON)
option(IRIS_WITH_EIGEN
  "C++ matrix library. Only disable if you have this already." ON)
option(IRIS_WITH_MOSEK
  "Convex optimization solver; free for academics. Only disable if you have this already."
  ON)
option(IRIS_WITH_CDD
  "Tool for converting representations of polytopes. Only disable if you have this already."
  ON)
option(IRIS_WITH_PYBIND11
  "Binding generator for Python based on C++11. Only disable if you have this already."
  ON)
option(IRIS_WITH_MATLAB "Install the pure-MATLAB version of IRIS" OFF)

set(IRIS_DEPENDENCIES)


if(IRIS_WITH_CDD)
  if(NOT CMAKE_VERSION VERSION_LESS 3.1)
    set(AUTOTOOLS_ENV
      "${CMAKE_COMMAND}" -E env
      "CC=${CMAKE_C_COMPILER}"
      "CFLAGS=${CMAKE_C_FLAGS}"
      "LDFLAGS=${CMAKE_SHARED_LINKER_FLAGS}")
  endif()

  find_program(PATCH_EXECUTABLE NAMES patch)
  mark_as_advanced(PATCH_EXECUTABLE)
  if(NOT PATCH_EXECUTABLE)
    message(FATAL_ERROR "Could NOT find patch executable")
  endif()

  set(MAKE_COMMAND "${CMAKE_MAKE_PROGRAM}")
  if(CMAKE_VERBOSE_MAKEFILE)
    set(MAKE_COMMAND "${MAKE_COMMAND}" V=1)
  endif()

  ExternalProject_Add(cdd
    DOWNLOAD_DIR "${CMAKE_CURRENT_BINARY_DIR}/cdd-download"
    URL https://d2tbce6hkathzp.cloudfront.net/other/cddlib/cddlib-094h.tar.gz
    URL_HASH SHA256=fe6d04d494683cd451be5f6fe785e147f24e8ce3ef7387f048e739ceb4565ab5
    TLS_VERIFY 1
    SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/cdd-src"
    PATCH_COMMAND "${PATCH_EXECUTABLE}" -p1 < "${CMAKE_CURRENT_SOURCE_DIR}/cdd.patch"
    CONFIGURE_COMMAND ${AUTOTOOLS_ENV} "<SOURCE_DIR>/configure" "--prefix=${CMAKE_INSTALL_PREFIX}"
    BUILD_COMMAND ${AUTOTOOLS_ENV} ${MAKE_COMMAND}
    BUILD_IN_SOURCE 1)
  ExternalProject_Get_Property(cdd SOURCE_DIR)
  ExternalProject_Add_Step(cdd install_setoper_header
    COMMAND "${CMAKE_COMMAND}" -E copy "${SOURCE_DIR}/lib-src/setoper.h" "${CMAKE_INSTALL_PREFIX}/include"
    DEPENDEES install
    COMMENT "installing setoper.h header manually")
  list(APPEND IRIS_DEPENDENCIES cdd)
endif()



list(INSERT CMAKE_PREFIX_PATH 0 "${CMAKE_INSTALL_PREFIX}")

set(IRIS_CMAKE_ARGS
  -DBUILD_TESTING=${BUILD_TESTING}
  -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  "-DCMAKE_C_COMPILER_LAUNCHER=${CMAKE_C_COMPILER_LAUNCHER}"
  "-DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}"
  "-DCMAKE_C_FLAGS=${CMAKE_C_FLAGS}"
  "-DCMAKE_CXX_COMPILER_LAUNCHER=${CMAKE_CXX_COMPILER_LAUNCHER}"
  "-DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}"
  "-DCMAKE_CXX_FLAGS=${CMAKE_CXX_FLAGS}"
  "-DCMAKE_EXE_LINKER_FLAGS=${CMAKE_EXE_LINKER_FLAGS}"
  "-DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}"
  "-DCMAKE_MODULE_LINKER_FLAGS=${CMAKE_MODULE_LINKER_FLAGS}"
  "-DCMAKE_MODULE_PATH=${CMAKE_MODULE_PATH}"
  "-DCMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}"
  "-DCMAKE_SHARED_LINKER_FLAGS=${CMAKE_SHARED_LINKER_FLAGS}"
  -DCMAKE_VERBOSE_MAKEFILE=${CMAKE_VERBOSE_MAKEFILE}
  -DPYBIND11_PYTHON_VERSION=${PYBIND11_PYTHON_VERSION}
  -DWITH_MATLAB=${IRIS_WITH_MATLAB})

if(DEFINED EIGEN3_INCLUDE_DIR)
  list(APPEND IRIS_CMAKE_ARGS "-DEIGEN3_INCLUDE_DIR=${EIGEN3_INCLUDE_DIR}")
endif()
if(DEFINED PYTHON_EXECUTABLE)
  list(APPEND IRIS_CMAKE_ARGS "-DPYTHON_EXECUTABLE=${PYTHON_EXECUTABLE}")
endif()
if(DEFINED PYTHON_INCLUDE_DIR)
  list(APPEND IRIS_CMAKE_ARGS "-DPYTHON_INCLUDE_DIR=${PYTHON_INCLUDE_DIR}")
endif()
if(DEFINED PYTHON_LIBRARY)
  list(APPEND IRIS_CMAKE_ARGS "-DPYTHON_LIBRARY=${PYTHON_LIBRARY}")
endif()

if(CMAKE_VERSION VERSION_LESS 3.2)
  set(EXTERNAL_PROJECT_ADD_BUILD_ALWAYS)
else()
  set(EXTERNAL_PROJECT_ADD_BUILD_ALWAYS BUILD_ALWAYS 1)
endif()

ExternalProject_Add(iris
  SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src"
  CMAKE_ARGS ${IRIS_CMAKE_ARGS}
  BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/iris-build"
  ${EXTERNAL_PROJECT_ADD_BUILD_ALWAYS}
  DEPENDS ${IRIS_DEPENDENCIES})

if(CMAKE_VERSION VERSION_LESS 3.2)
  ExternalProject_Add_Step(iris build_always
    COMMAND "${CMAKE_COMMAND}" -E echo "Force configure of IRIS"
    DEPENDEES update
    DEPENDERS configure
    ALWAYS 1)
endif()
