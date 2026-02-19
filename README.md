# Kalibr Docker

Docker wrapper around the mrs fork of ethz-asl/kalibr

1. `cd compose_session`
2. Pull the docker image by calling `docker compose pull`
3. Store your images in the [data/camera](./compose_session/data/camera) folder and retrieve the results in [data](./compose_session/data) afterwards.
4. Configure the parameters by editing the `compose_session/compose.yaml` file.
5. Use [run.sh](./compose_session/run.sh) to start the [compose](./compose_session/compose.yaml) session with kalibr.

## How to generate a sequence of images from rosbags

This repo includes tools for extracting images from ROS1 and ROS2 bagfiles in the [input_conversion/scripts](./input_conversion/scripts/) folder. But they only support compressed image topics, an alternative is described [here](https://ctu-mrs.github.io/docs/simulations/gazebo/gazebo_video#3-generate-sequence-of-images-from-rosbag).

If the output directory is not specified, the extracted images will be placed in [compose_session/data/camera](./compose_session/data/camera), therefore the full pipeline can be ran with:

```bash
bash input_conversion/run.sh ros.mcap /camera/rgb/image_raw
bash compose_session/run.sh
```

## Troubleshooting

If a calibration can not be found for the pinhole-radtan model, try to find it for the pinhole-equi model first. Then, initialize the focal lenght in the compose file using the one you obtained from the calibration (the first element of the projection matrix).

## Output conversion to the `camera_calibration` format

Use the script in [output_conversion](./output_conversion) to convert the Kalibr format (with the `radtan` model) to the output of `camera_calibration`.
