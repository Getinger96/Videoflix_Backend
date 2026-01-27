import subprocess
import os




def convert_720p(source):
    base, _ = os.path.splitext(source)
    target = base + "_720p.mp4"

    cmd = [
        "ffmpeg",
        "-y",
        "-i", source,
        "-vf", "scale=-2:720",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        target
    ]

    subprocess.run(cmd, check=True)


def convert_480p(source):
    base, _ = os.path.splitext(source)
    target = base + "_480p.mp4"

    cmd = [
        "ffmpeg",
        "-y",
        "-i", source,
        "-vf", "scale=-2:480",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        target
    ]

    subprocess.run(cmd, check=True)


def convert_1080p(source):
    base, _ = os.path.splitext(source)
    target = base + "_1080p.mp4"

    cmd = [
        "ffmpeg",
        "-y",
        "-i", source,
        "-vf", "scale=-2:1080",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        target
    ]

    subprocess.run(cmd, check=True)



def convert_all(path):
    convert_720p(path)
    convert_480p(path)
    convert_1080p(path)