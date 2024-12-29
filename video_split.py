#!/usr/bin/python

import subprocess
import os
import re

from video_utils import *

def main(seg_sec_duration):
    split_video(seg_sec_duration)
    print("Video splitting completed for all qualities.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 ", sys.argv[0], " <video segment duration in sec>")
    else:
        main(sys.argv[1])

