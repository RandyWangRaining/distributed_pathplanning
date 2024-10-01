#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "iris::iris_cvxgen_ldp" for configuration "Release"
set_property(TARGET iris::iris_cvxgen_ldp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(iris::iris_cvxgen_ldp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libiris_cvxgen_ldp.so.0"
  IMPORTED_SONAME_RELEASE "libiris_cvxgen_ldp.so.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS iris::iris_cvxgen_ldp )
list(APPEND _IMPORT_CHECK_FILES_FOR_iris::iris_cvxgen_ldp "${_IMPORT_PREFIX}/lib/libiris_cvxgen_ldp.so.0" )

# Import target "iris::iris_cvxgen_ldp_cpp" for configuration "Release"
set_property(TARGET iris::iris_cvxgen_ldp_cpp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(iris::iris_cvxgen_ldp_cpp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libiris_cvxgen_ldp_cpp.so.0"
  IMPORTED_SONAME_RELEASE "libiris_cvxgen_ldp_cpp.so.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS iris::iris_cvxgen_ldp_cpp )
list(APPEND _IMPORT_CHECK_FILES_FOR_iris::iris_cvxgen_ldp_cpp "${_IMPORT_PREFIX}/lib/libiris_cvxgen_ldp_cpp.so.0" )

# Import target "iris::iris" for configuration "Release"
set_property(TARGET iris::iris APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(iris::iris PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libiris.so.0"
  IMPORTED_SONAME_RELEASE "libiris.so.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS iris::iris )
list(APPEND _IMPORT_CHECK_FILES_FOR_iris::iris "${_IMPORT_PREFIX}/lib/libiris.so.0" )

# Import target "iris::iris_geometry" for configuration "Release"
set_property(TARGET iris::iris_geometry APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(iris::iris_geometry PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libiris_geometry.so.0"
  IMPORTED_SONAME_RELEASE "libiris_geometry.so.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS iris::iris_geometry )
list(APPEND _IMPORT_CHECK_FILES_FOR_iris::iris_geometry "${_IMPORT_PREFIX}/lib/libiris_geometry.so.0" )

# Import target "iris::iris_mosek" for configuration "Release"
set_property(TARGET iris::iris_mosek APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(iris::iris_mosek PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libiris_mosek.so.0"
  IMPORTED_SONAME_RELEASE "libiris_mosek.so.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS iris::iris_mosek )
list(APPEND _IMPORT_CHECK_FILES_FOR_iris::iris_mosek "${_IMPORT_PREFIX}/lib/libiris_mosek.so.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
