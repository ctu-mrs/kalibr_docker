#!/usr/bin/env python3

from argparse import ArgumentParser
from os import makedirs, path
from rosbag import Bag

def main():
    parser = ArgumentParser(description='Extract images from a ROS bag.')
    parser.add_argument('bag_file', help='Input ROS bag.')
    parser.add_argument('image_topic', help='Image topic.')
    parser.add_argument('output_dir', help='Output directory.')

    args = parser.parse_args()
    makedirs(args.output_dir, exist_ok=True)

    count = 0
    with Bag(args.bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=[args.image_topic]):
            # We grab the raw byte array directly from the message
            byte_stream = msg.data

            # We determine extension based on the message format string
            ext = 'png' if 'png' in msg.format else 'jpg'
            filename = path.join(
                args.output_dir,
                f'frame_{msg.header.stamp}.{ext}'
            )

            # Write bytes directly to file (No OpenCV involved)
            with open(filename, 'wb') as f:
                f.write(byte_stream)

            count += 1

    print(f'Dumped {count} raw image files.')

if __name__ == '__main__':
    main()
