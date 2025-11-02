# Root CMakeLists.txt

cmake_minimum_required(VERSION 3.14)
project(MyProject VERSION 1.0.0 LANGUAGES CXX)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)
# Include directories
include_directories(${PROJECT_SOURCE_DIR}/include)

message(STATUS "Build type: ${BUILD_TYPE_CACHE}") #this variable is used in msvc compiler because it needs to be passed in during build not configure
if(MSVC)
    message(STATUS "Detected compiler: MSVC (Visual Studio)")
    message(STATUS "Target system: Windows")
    add_compile_options(/W4 /permissive-)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    message(STATUS "Detected compiler: GCC")
    message(STATUS "Target system: Linux/Unix")
    add_compile_options(-Wall -Wextra -O2)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    message(STATUS "Detected compiler: Clang")
    message(STATUS "Target system: Linux/Unix")
    add_compile_options(-Wall -Wextra -O2)
endif()

# Add subdirectories for src, app, and third_party
add_subdirectory(src)
add_subdirectory(app)
# add_subdirectory(external)

