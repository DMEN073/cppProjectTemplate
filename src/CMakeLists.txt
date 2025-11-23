# src/lib/CMakeLists.txt

# Define the MyLib library target
add_library(MyLib SHARED mylib.cpp)

# Specify include directories for MyLib
target_include_directories(MyLib PUBLIC ${PROJECT_SOURCE_DIR}/include)

# Set per-config output for MSVC
if(MSVC)
    set_target_properties(MyLib PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib/$<CONFIG>
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin/$<CONFIG>
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin/$<CONFIG>
    )
endif()
