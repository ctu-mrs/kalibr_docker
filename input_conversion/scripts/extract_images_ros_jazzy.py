#!/usr/bin/env python3

from argparse import ArgumentParser
from os import makedirs, path

from rclpy.serialization import deserialize_message
from rosbag2_py import ConverterOptions, SequentialReader, StorageOptions
from sensor_msgs.msg import CompressedImage

def main():
    parser = ArgumentParser(description='Extract images from a ROS2 bag.')
    parser.add_argument('bag_file', help='Input ROS2 bag.')
    parser.add_argument('image_topic', help='Image topic.')
    parser.add_argument('output_dir', help='Output directory.')

    args = parser.parse_args()
    makedirs(args.output_dir, exist_ok=True)

    reader = SequentialReader()
    storage_options = StorageOptions(
        uri=args.bag_file,
        storage_id='mcap' if args.bag_file.endswith('.mcap') else 'sqlite3'
    )

    converter_options = ConverterOptions('cdr', 'cdr')
    reader.open(storage_options, converter_options)

    count = 0
    while reader.has_next():
        topic, data, t = reader.read_next()
        if topic != args.image_topic:
            continue

        # We grab the raw byte array directly from the message
        msg = deserialize_message(data, CompressedImage)
        byte_stream = msg.data

        # We determine extension based on the message format string
        ext = 'png' if 'png' in msg.format else 'jpg'
        filename = path.join(
            args.output_dir,
            f'frame_{msg.header.stamp.sec}_{msg.header.stamp.nanosec}.{ext}'
        )

        # Write bytes directly to file (No OpenCV involved)
        with open(filename, 'wb') as f:
            f.write(byte_stream)

        count += 1

    print(f'Dumped {count} raw image files.')

if __name__ == '__main__':
    main()
