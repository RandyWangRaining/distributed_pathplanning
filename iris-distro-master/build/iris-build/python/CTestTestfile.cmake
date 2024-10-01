# CMake generated Testfile for 
# Source directory: /home/randywang/pathplanning/distributedplanning/iris-distro-master/src/python
# Build directory: /home/randywang/pathplanning/distributedplanning/iris-distro-master/build/iris-build/python
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(python_tests "/usr/bin/python3" "-m" "nose" "--nocapture" "irispy")
set_tests_properties(python_tests PROPERTIES  ENVIRONMENT "PYTHONPATH=/home/randywang/pathplanning/distributedplanning/iris-distro-master/build/install/lib/python3.8/dist-packages" _BACKTRACE_TRIPLES "/home/randywang/pathplanning/distributedplanning/iris-distro-master/src/python/CMakeLists.txt;4;add_test;/home/randywang/pathplanning/distributedplanning/iris-distro-master/src/python/CMakeLists.txt;0;")
