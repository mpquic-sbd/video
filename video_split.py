#!/usr/bin/python

import subprocess
import os
import re

from video_utils import *

#def split_video(seg_sec_duration, fmpd = "output_dash.mpd", isSegmentTemplate = False)

def main(seg_sec_duration):
    split_video(seg_sec_duration, "output_dash_template.mpd", True)
    run_cmd(["rm", "*.m4s"])
    split_video(seg_sec_duration, "output_dash.mpd", False)

    run_cmd(["python3", "video_sara_mpd.py", "output_dash_template.mpd"])
    dir_name = f"{seg_sec_duration}s"
    run_cmd(["mkdir", dir_name])
    run_cmd(["mv", "segment_*", dir_name])
    run_cmd(["mv", "output_dash*", dir_name])

    print("Video splitting completed for all qualities.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 ", sys.argv[0], " <video segment duration in sec>")
    else:
        main(sys.argv[1])

