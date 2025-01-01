import subprocess
import os
import re

debug_dont_run = False

def get_video_qualities():
    return [
        {"#": 1,  "Quality": "21602p, 60 fps", "Resolution": "3840x2160", "Bitrate": 20000},
        {"#": 2,  "Quality": "2160p, 30 fps",  "Resolution": "3840x2160", "Bitrate": 15000},
        {"#": 3,  "Quality": "14402p, 60 fps", "Resolution": "2560x1440", "Bitrate": 10000},
        {"#": 4,  "Quality": "1440p, 30 fps",  "Resolution": "2560x1440", "Bitrate": 6000},
        {"#": 5,  "Quality": "10802p, 60 fps", "Resolution": "1920x1080", "Bitrate": 4500},
        {"#": 6,  "Quality": "1080p, 25 fps",  "Resolution": "1920x1080", "Bitrate": 3000},
        {"#": 7,  "Quality": "7202p, 60 fps",  "Resolution": "1280x720",  "Bitrate": 2250},
        {"#": 8,  "Quality": "720p, 25 fps",   "Resolution": "1280x720",  "Bitrate": 1500},
        {"#": 9,  "Quality": "480p, 25 fps",   "Resolution": "854x480",   "Bitrate": 500},
        {"#": 10, "Quality": "360p, 25 fps",   "Resolution": "640x360",   "Bitrate": 400},
        {"#": 11, "Quality": "240p, 25 fps",   "Resolution": "426x240",   "Bitrate": 300},
    ]

def run_cmd(command):
    cmd = ' '.join(str(c) for c in command)
    print(cmd)
    if debug_dont_run is True:
       return
    result = subprocess.run(cmd, shell=True, check=True, universal_newlines=False)
    print(f"Command output: {result.stdout}")
    if result.stderr:
        print(f"Command error: {result.stderr}")
    result.check_returncode()

def download_video(url):
    file_extension = re.search(r"\.\w+$", url).group(0)
    if file_extension not in [".mp4", ".webm"]:
        raise ValueError("Only .mp4 and .webm are supported.")

    output_file = f"downloaded_video{file_extension}"
    cmd = ["wget", "-O", output_file, url]
    run_cmd(cmd)
    return output_file

def get_convert_video_cmd(input_file, output_file, resolution, bitrate, fps):
    cmd = [
        "ffmpeg -y",
        "-i", f"{input_file}",
        "-c:a", "aac",
        "-ac", "2",
        "-b:a", "128k",
        "-c:v", "libx264",
        "-x264opts", '"keyint=96:min-keyint=96:no-scenecut"',
        "-b:v", f"{bitrate}k",
        "-maxrate", f"{2*bitrate}k",
        "-bufsize", "1000k",
        "-s", f"{resolution}",
        "-vf", f"scale={resolution}",
        "-filter:v", f"fps={fps}",
        f"{output_file}",
        "&"]
    return cmd

def get_fps(quality):
    return quality.split(" ")[1]

def get_id(quality):
    return quality.split(" ")[0].split(",")[0]

def split_video(seg_sec_duration, fmpd = "output_dash.mpd", isSegmentTemplate = False):
    qualities = get_video_qualities()
    cmd = [
        'MP4Box',
        '-dash', int(seg_sec_duration) * 1000,
        '-segment-name', "'segment_$RepresentationID$_$Number$'",
        '-mpd-refresh', seg_sec_duration,
	'-bs-switching', 'no'
        ]

    if isSegmentTemplate is True:
        cmd.append('-url-template')

    for quality in qualities:
        fps = get_fps(quality['Quality'])
        output_video = f"video_{quality['Quality'].replace(':', '').replace(',', '').replace(' ', '_')}.mp4"
        id = get_id(quality['Quality'])
        cmd.append(f'-fps {fps}')
        cmd.append(f'{output_video}#video:id={id}')

    cmd.append(f"-out {fmpd}")
    run_cmd(cmd)

def process_video_qualities(input_file):
    qualities = get_video_qualities()
    output_files = []
    for quality in qualities:
        resolution = quality["Resolution"]
        bitrate = quality["Bitrate"]
        fps = get_fps(quality['Quality'])
        output_video = f"video_{quality['Quality'].replace(':', '').replace(',', '').replace(' ', '_')}.mp4"
        output_files.append(output_video)
        cmd = get_convert_video_cmd(input_file, output_video, resolution, bitrate, fps)
        run_cmd(cmd)
    return output_files

