#!/usr/bin/python

import subprocess
import os
import re

from video_utils import *

#def split_video(seg_sec_duration, fmpd = "output_dash.mpd", isSegmentTemplate = False)

def main(seg_sec_duration):
    # for sara abr, generate an mpd with the SegmentTemplate tag
    split_video(seg_sec_duration, "output_dash_template.mpd", True)
    run_cmd(["rm", "*.m4s"])
    # for the other abrs, generate default mpd file
    split_video(seg_sec_duration, "output_dash.mpd", False)
    # from the SegmentTemplate mpd, generate mpd for sara
    run_cmd(["python3", "video_sara_mpd.py", "output_dash_template.mpd"])
    # move relevant files out to the resulting segment folder
    dir_name = f"{seg_sec_duration}s"
    run_cmd(["mkdir", dir_name])
    run_cmd(["mv", "segment_*", dir_name])
    run_cmd(["rm", "output_dash_template*"])
    run_cmd(["mv", "output_dash*", dir_name])
    # for bulk transfer, create a link to the original downloaded video file inside the resulting segment folder
    os.chdir(dir_name)
    run_cmd(["ln", "-s", "../downloaded_video.webm"])
    os.chdir("../")

    print("Video splitting completed for all qualities.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 ", sys.argv[0], " <video segment duration in sec>")
    else:
        main(sys.argv[1])

