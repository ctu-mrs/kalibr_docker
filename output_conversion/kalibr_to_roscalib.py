#!/usr/bin/python3

import yaml
import cv2
import numpy

def main():

    input_path = "./camera_front-camchain.yaml"
    output_path = "./roscalib.yaml"

    with open(input_path, "r") as input_file:

        try:
            data = yaml.safe_load(input_file)
        except yaml.YAMLError as exc:
            print(exc)

        for camera in data:

            properties = data[camera]

            cam_overlaps = properties['cam_overlaps']
            print("cam_overlaps: {}".format(cam_overlaps))

            camera_model = properties['camera_model']
            print("camera_model: {}".format(camera_model))

            distortion_coeffs = properties['distortion_coeffs']
            print("distortion_coeffs: {}".format(distortion_coeffs))

            distortion_model = properties['distortion_model']
            print("distortion_model: {}".format(distortion_model))

            intrinsics = properties['intrinsics']
            print("intrinsics: {}".format(intrinsics))

            resolution = properties['resolution']
            print("resolution: {}".format(resolution))

            rostopic = properties['rostopic']
            print("rostopic: {}".format(rostopic))

            print("")
            print("")

            if distortion_model != "radtan":
                print("Error: the distortion model needs to be radtan")
                exit()

            intrinsics_1d_mat = [intrinsics[0], 0, intrinsics[2], 0, intrinsics[1], intrinsics[3], 0, 0, 1.0]

            distortion_1d_mat = [distortion_coeffs[0], distortion_coeffs[1], distortion_coeffs[2], distortion_coeffs[3], 0.0]

            size = (resolution[0], resolution[1])

            C = numpy.array(intrinsics_1d_mat, dtype=numpy.float64, copy=True).reshape((3, 3))
            D = numpy.array(distortion_1d_mat, dtype=numpy.float64, copy=True).reshape((len(distortion_1d_mat), 1))

            P, _ = cv2.getOptimalNewCameraMatrix(C, D, size, 1.0)

            P_1d_mat = numpy.hstack((P, numpy.array([[0], [0], [0]]))).reshape(1, 12).tolist()

            output_data = {
                "image_width" : resolution[0],
                "image_height" : resolution[1],
                "camera_name" : rostopic.split("/")[2],
                "camera_matrix" : {
                    "rows" : 3,
                    "cols" : 3,
                    "data" : intrinsics_1d_mat,
                },
                "rectification_matrix" : {
                    "rows" : 3,
                    "cols" : 3,
                    "data" : [1.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 1.000000],
                },
                "distortion_model" : "plumb_bob",
                "distortion_coefficients" : {
                    "rows" : 1,
                    "cols" : 5,
                    "data" : distortion_1d_mat,
                },
                "projection_matrix" : {
                    "rows" : 3,
                    "cols" : 4,
                    "data" : P_1d_mat[0],
                },
            }

            with open(output_path, 'w') as outfile:
                yaml.dump(output_data, outfile, default_flow_style=None, sort_keys=False)

if __name__ == '__main__':
    main()
