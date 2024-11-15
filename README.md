# Kalibr Docker

Docker wrapper around ethz-asl/kalibr

1. `cd compose_session`
2. Pull the docker image by calling `docker compose pull`
3. Store your bag file in the [data](./compose_session/data) folder and retrieve the results there afterwards.
4. Configure the parameters by editing the `./compose_session/compose.yaml` file.
5. Use [run.sh](./compose_session/run.sh) to start the [compose](./compose_session/compose.yaml) session with kalibr.

## Output conversion to the `camera_calibration` format

Use the script in [./output_conversion](./output_conversion) to conver a calibr format (with the `radtan` model) to the output of `camera_calibration`;
