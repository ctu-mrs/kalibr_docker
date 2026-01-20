# Kalibr Docker

Docker wrapper around ethz-asl/kalibr

1. `cd compose_session`
2. Pull the docker image by calling `docker compose pull`
3. Store your images in the [data/camera](./compose_session/data/camera) folder and retrieve the results in [data](./compose_session/data) afterwards.
4. Configure the parameters by editing the `./compose_session/compose.yaml` file.
5. Use [run.sh](./compose_session/run.sh) to start the [compose](./compose_session/compose.yaml) session with kalibr.

## How to generate a sequence of images from rosbags

The following shell commands can be used for extracting images from a rosbag, [source](https://ctu-mrs.github.io/docs/simulations/gazebo/gazebo_video#3-generate-sequence-of-images-from-rosbag).

```bash
ros2 bag play rosbag2_with_recorded_image.mcap < /dev/null &
ros2 run image_view image_saver --ros-args \
  -r image:=/camera/rgb/image_raw \
  -p filename_format:=frame%06i.png \
  -p image_transport:=compressed
```

## Troubleshooting

If a calibration can not be found for the pinhole-radtan model, try to find it for the pinhole-equi model first.
Then, initialize the focal lenght in the compose file using the one you obtained from the calibration (the first element of the projection matrix).

## Output conversion to the `camera_calibration` format

Use the script in [./output_conversion](./output_conversion) to convert the Kalibr format (with the `radtan` model) to the output of `camera_calibration`;
