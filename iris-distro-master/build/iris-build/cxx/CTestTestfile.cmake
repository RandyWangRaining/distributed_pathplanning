# CMake generated Testfile for 
# Source directory: /home/randywang/pathplanning/distributedplanning/iris-distro-master/src/cxx
# Build directory: /home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(irisDemo "/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/cxx/irisDemo")
set_tests_properties(irisDemo PROPERTIES  _BACKTRACE_TRIPLES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/src/cxx/CMakeLists.txt;76;add_test;/home/randywang/pathplanning/distributedplanning/iris-distro-master/src/cxx/CMakeLists.txt;0;")
subdirs("cvxgen")
subdirs("test")
