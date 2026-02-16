#!/usr/bin/env python3
import os
import argparse
import cv2
import rosbag
from cv_bridge import CvBridge

def main():
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("image_topic", help="Image topic.")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    count = 0

    with rosbag.Bag(args.bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=[args.image_topic]):
            # We grab the raw byte array directly from the message
            byte_stream = msg.data
            
            # We determine extension based on the message format string
            # (e.g., "jpeg" or "png")
            ext = "png" if "png" in msg.format else "jpg"
            
            filename = os.path.join(args.output_dir, f"frame_{msg.header.stamp}.{ext}")
            
            # Write bytes directly to file (No OpenCV involved)
            with open(filename, "wb") as f:
                f.write(byte_stream)
            count += 1
    
    print(f"Dumped {count} raw image files.")
if __name__ == '__main__':
    main()
