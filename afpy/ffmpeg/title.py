import subprocess, sys, argparse
from pathlib import Path


def run_ffmpeg(duration, color, output_file, title, subtitle):
    vf = (
        f"drawtext=text='{title}':fontfile=/path/to/font.ttf:"
        f"x=(w-text_w)/2:y=(h/2-50):fontsize=72:fontcolor=white,"
        f"drawtext=text='{subtitle}':fontfile=/path/to/font.ttf:"
        f"x=(w-text_w)/2:y=(h/2+50):fontsize=48:fontcolor=white,"
        f"fade=t=in:st=0:d=1,fade=t=out:st={duration-1}:d=1"
    )

    cmd = [
        "ffmpeg",
        "-f",
        "lavfi",
        "-i",
        f"color=c={color}:s=1920x1080:d={duration}",
        "-f",
        "lavfi",
        "-i",
        f"anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-shortest",
        output_file,
        "-y",
    ]
    subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )


def setup_parser(parser):
    parser.description = "Generate a title slide."
    parser.add_argument(
        "--duration", type=int, default=5, help="Video duration in seconds (default 5)."
    )
    parser.add_argument(
        "--color", default="black", help="Background color (default black)."
    )
    parser.add_argument("--output-file", required=True, help="Output video file path.")
    parser.add_argument("--title", required=True, help="Main title text.")
    parser.add_argument("--subtitle", required=True, help="Subtitle text.")
    return parser


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    setup_parser(parser)
    args = parser.parse_args(args)

    run_ffmpeg(args.duration, args.color, args.output_file, args.title, args.subtitle)


if __name__ == "__main__":
    main()
