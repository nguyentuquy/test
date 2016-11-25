cmake_minimum_required(VERSION 2.8.3)
project(qw)


## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS roscpp geometry_msgs joy)

include_directories(${catkin_INCLUDE_DIRS})

catkin_package(
  INCLUDE_DIRS
  LIBRARIES move
  CATKIN_DEPENDS roscpp geometry_msgs
  DEPENDS
)

add_executable(move src/move.cpp)
target_link_libraries(move ${catkin_LIBRARIES})

## Mark executables and/or libraries for installation
install(TARGETS move  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## Mark all other useful stuff for installation
install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

#auto_move
add_executable(auto_move src/auto_move.cpp)
target_link_libraries(auto_move ${catkin_LIBRARIES})


#collision
add_executable(collision src/collision.cpp)
target_link_libraries(collision ${catkin_LIBRARIES})

