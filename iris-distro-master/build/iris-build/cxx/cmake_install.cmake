# Install script for directory: /home/randywang/pathplanning/distributedplanning/iris-distro-master/src/cxx

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so.0")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so.0"
         RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/libiris.so.0")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so.0")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so.0"
         OLD_RPATH "/home/randywang/mosek/8/tools/platform/linux64x86/bin:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/cvxgen:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:"
         NEW_RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so.0")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so"
         RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/libiris.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so"
         OLD_RPATH "/home/randywang/mosek/8/tools/platform/linux64x86/bin:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/cvxgen:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:"
         NEW_RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/iris" TYPE FILE FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/src/cxx/iris/iris.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so.0")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so.0"
         RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/libiris_geometry.so.0")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so.0")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so.0"
         OLD_RPATH "/home/randywang/mosek/8/tools/platform/linux64x86/bin:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:"
         NEW_RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so.0")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so"
         RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/libiris_geometry.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so"
         OLD_RPATH "/home/randywang/mosek/8/tools/platform/linux64x86/bin:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:"
         NEW_RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_geometry.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/iris" TYPE FILE FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/src/cxx/iris/geometry.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so.0")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so.0"
         RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/libiris_mosek.so.0")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so.0")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so.0"
         OLD_RPATH "/home/randywang/mosek/8/tools/platform/linux64x86/bin:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:"
         NEW_RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so.0")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so"
         RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/libiris_mosek.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so"
         OLD_RPATH "/home/randywang/mosek/8/tools/platform/linux64x86/bin:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:"
         NEW_RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libiris_mosek.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/iris" TYPE FILE FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/src/cxx/iris/iris_mosek.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/iris.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/iris/iris-targets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/iris/iris-targets.cmake"
         "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/CMakeFiles/Export/lib/cmake/iris/iris-targets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/iris/iris-targets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/iris/iris-targets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/iris" TYPE FILE FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/CMakeFiles/Export/lib/cmake/iris/iris-targets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/iris" TYPE FILE FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/CMakeFiles/Export/lib/cmake/iris/iris-targets-release.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/iris" TYPE FILE FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/iris-config.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.8/dist-packages/irispy/iris_wrapper.cpython-38-x86_64-linux-gnu.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.8/dist-packages/irispy/iris_wrapper.cpython-38-x86_64-linux-gnu.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.8/dist-packages/irispy/iris_wrapper.cpython-38-x86_64-linux-gnu.so"
         RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3.8/dist-packages/irispy" TYPE MODULE FILES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/iris_wrapper.cpython-38-x86_64-linux-gnu.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.8/dist-packages/irispy/iris_wrapper.cpython-38-x86_64-linux-gnu.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.8/dist-packages/irispy/iris_wrapper.cpython-38-x86_64-linux-gnu.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.8/dist-packages/irispy/iris_wrapper.cpython-38-x86_64-linux-gnu.so"
         OLD_RPATH "/home/randywang/mosek/8/tools/platform/linux64x86/bin:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/cvxgen:/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:"
         NEW_RPATH "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib:/home/randywang/mosek/8/tools/platform/linux64x86/bin")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.8/dist-packages/irispy/iris_wrapper.cpython-38-x86_64-linux-gnu.so")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/cvxgen/cmake_install.cmake")
  include("/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/test/cmake_install.cmake")

endif()

