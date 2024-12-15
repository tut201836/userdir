#!/bin/bash

DOCKER_MOUNT_DIR="/bwc_ws"
MC_RTC_WORKSPCE=/mc_rtc_ws

REPOSITORY=isri-aist
COMMIT_SHA=master

set -x 
function build () {
    source /opt/ros/noetic/setup.bash
    source ${MC_RTC_WORKSPCE}/src/catkin_ws/devel/setup.bash
    source /ros_ws/devel/setup.bash
    rosdep update
    rosdep install -y -r --from-paths src --ignore-src
    catkin build baseline_footstep_planner -DCMAKE_BUILD_TYPE=RelWithDebInfo 
    PATH=${MC_RTC_WORKSPCE}/install/lib/cmake:$PATH catkin build baseline_walking_controller -DCMAKE_BUILD_TYPE=RelWithDebInfo -DENABLE_QLD=ON
}

function clone () {
    source /opt/ros/noetic/setup.bash
    source ${MC_RTC_WORKSPCE}/src/catkin_ws/devel/setup.bash
    source /ros_ws/devel/setup.bash
    wstool init src
    mkdir -p src/isri-aist/BaselineWalkingController
    cd src/isri-aist/BaselineWalkingController
    git init
    git remote add origin https://github.com/$1/BaselineWalkingController
    git fetch origin $2
    git checkout $2
    git submodule update --init --recursive
    cd ${DOCKER_MOUNT_DIR}
    wstool merge -t src src/isri-aist/BaselineWalkingController/depends.rosinstall
    wstool update -t src
}


cd ${DOCKER_MOUNT_DIR}

if [ -e "src/isri-aist/BaselineWalkingController" ]; then
    build
else 
    clone ${REPOSITORY} ${COMMIT_SHA}
    build
fi