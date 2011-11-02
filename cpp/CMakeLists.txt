cmake_minimum_required(VERSION 2.8)

file(GLOB HEADERS "*.h")

# Library targets:
#   nanomunchers_serialize - serialization code library
project(nanomunchers_serialize)
set(SRCS
    "nanomunchers_serialize.cpp")
  add_library(nanomunchers_serialize STATIC ${SRCS} ${HEADERS})

# Executable targets:
#   nanomuncher_serialize_gtest - serialization code gtests

# Only build when GTest set specifically since we dont distribute GTest
# with this source tree.
if(HPS_GTEST_ENABLED)
  project(nanomunchers_serialize_gtest)
  set(SRCS
      "nanomunchers_serialize_gtest.cpp")
  include_directories(${GTEST_INCLUDE_DIRS})
  add_executable(nanomunchers_serialize_gtest ${SRCS} ${HEADERS})
  target_link_libraries(nanomunchers_serialize_gtest nanomunchers_serialize gtest)
  add_test(nanomunchers_serialize_gtest nanomunchers_serialize_gtest)
  # Copy data files to build directory.
  set(DATA_FILES "data_0" "data_1")
  file(COPY ${DATA_FILES} DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
endif(HPS_GTEST_ENABLED)

project(nanomunchers_serialize_all)
