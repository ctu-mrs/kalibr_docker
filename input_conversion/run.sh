#!/bin/bash

bag_file="$(realpath "${1:-ros.mcap}")"
bag_file_name="$(basename "$bag_file")"
image_topic="${2:-/camera/rgb/image_raw}"

this_dir="$(dirname "$(realpath "$0")")"
output_dir="${3:-$this_dir/../compose_session/data/camera}"

ros='jazzy'
if [ "$(head -c 4 "$bag_file" 2> /dev/null)" = '#ROS' ]; then
  ros='noetic'
fi

docker run --rm \
  -v "$bag_file":"/tmp/$bag_file_name" \
  -v "$this_dir/scripts/extract_images_ros_$ros.py":/tmp/extract_images_ros.py \
  -v "$output_dir":/tmp/camera \
  ctumrs/ros_$ros:latest python3 \
  /tmp/extract_images_ros.py "/tmp/$bag_file_name" "$image_topic" /tmp/camera
