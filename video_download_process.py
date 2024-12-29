#!/usr/bin/python

import subprocess
import os
import re

from video_utils import *

def main(video_url):
    input_file = download_video(video_url)
    output_files = process_video_qualities(input_file)
    print("Video conversion completed for all qualities.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 ", sys.argv[0], " <video_url>")
    else:
        main(sys.argv[1])

#python3  https://upload.wikimedia.org/wikipedia/commons/d/de/The_Earth-_4K_Extended_Edition.webm
