cmake_minimum_required(VERSION 3.5)

project(MDI
        LANGUAGES C CXX Fortran)

find_package(MPI)

if(MPI_FOUND)
   include_directories(${MPI_INCLUDE_PATH})
else()
   include_directories(${CMAKE_SOURCE_DIR}/STUBS_MPI/)
endif()

set( MDI_LOCATION ${CMAKE_SOURCE_DIR}/../lib/mdi_build/molssi_driver_interface/ )
link_directories( ${MDI_LOCATION} )




add_executable(md
           md.cpp)
target_link_libraries(md mdi
                                 ${MPI_LIBRARIES})
set_target_properties(md
                      PROPERTIES LINKER_LANGUAGE CXX)

if(MPI_COMPILE_FLAGS)
  set_target_properties(md PROPERTIES
    COMPILE_FLAGS "${MPI_COMPILE_FLAGS}")
endif()

if(MPI_LINK_FLAGS)
  set_target_properties(md PROPERTIES
    LINK_FLAGS "${MPI_LINK_FLAGS}")
endif()




# copy MDI python files
#configure_file(${MDI_LOCATION}/mdi.py ${CMAKE_CURRENT_BINARY_DIR}/mdi/mdi.py COPYONLY)
#configure_file(${MDI_LOCATION}/__init__.py ${CMAKE_CURRENT_BINARY_DIR}/mdi/__init__.py COPYONLY)
file(COPY ${MDI_LOCATION} DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/mdi)

# copy MDI_examples python files
configure_file(${CMAKE_SOURCE_DIR}/md.py ${CMAKE_CURRENT_BINARY_DIR}/md.py COPYONLY)
configure_file(${CMAKE_SOURCE_DIR}/aimd.py ${CMAKE_CURRENT_BINARY_DIR}/aimd.py COPYONLY)
configure_file(${CMAKE_SOURCE_DIR}/md_qmmm_comm.py ${CMAKE_CURRENT_BINARY_DIR}/md_qmmm_comm.py COPYONLY)
