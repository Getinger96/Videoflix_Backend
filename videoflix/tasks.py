import subprocess
import os


def convert_to_hls(source, movie_id, resolution, height):
    output_dir = f"media/hls/{movie_id}/{resolution}"
    os.makedirs(output_dir, exist_ok=True)

    playlist = os.path.join(output_dir, "index.m3u8")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", source,
        "-vf", f"scale=-2:{height}",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-crf", "20",
        "-g", "48",
        "-keyint_min", "48",
        "-sc_threshold", "0",
        "-c:a", "aac",
        "-ar", "48000",
        "-hls_time", "4",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", f"{output_dir}/%03d.ts",
        playlist
    ]

    subprocess.run(cmd, check=True)


def convert_all(source, movie_id):
    convert_to_hls(source, movie_id, "480p", 480)
    convert_to_hls(source, movie_id, "720p", 720)
    convert_to_hls(source, movie_id, "1080p", 1080)
