import subprocess
import os


def convert_to_hls(source, movie_id, resolution, height):
    """
    Convert a video file into an HLS stream for a specific resolution.

    This function uses FFmpeg to:
    - Scale the video to the given height
    - Encode the video using H.264
    - Split the video into HLS (.ts) segments
    - Generate an HLS playlist (index.m3u8)

    :param source: Path to the source video file
    :param movie_id: ID of the video (used for directory structure)
    :param resolution: Resolution label (e.g. "480p", "720p")
    :param height: Target video height in pixels
    """

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
    """
    Convert a video file into multiple HLS resolutions.

    This function generates HLS streams for:
    - 480p
    - 720p
    - 1080p

    :param source: Path to the source video file
    :param movie_id: ID of the video
    """

    convert_to_hls(source, movie_id, "480p", 480)
    convert_to_hls(source, movie_id, "720p", 720)
    convert_to_hls(source, movie_id, "1080p", 1080)