import yaml, sys, argparse, subprocess, shutil
from pathlib import Path

try:
    import concatenate
    import title
except:
    from . import concatenate
    from . import title


def images_to_side_by_side_video(
    left_image: Path, right_image: Path, output: Path, duration: int = 5
):
    filter_complex = (
        "[0:v]scale=w=960:h=1080:force_original_aspect_ratio=increase,"
        "crop=960:1080,setsar=1[img1];"
        "[1:v]scale=w=960:h=1080:force_original_aspect_ratio=increase,"
        "crop=960:1080,setsar=1[img2];"
        "[img1][img2]hstack=inputs=2[out]"
    )

    cmd = [
        "ffmpeg",
        "-loop",
        "1",
        "-t",
        "5",
        "-i",
        str(left_image),
        "-loop",
        "1",
        "-t",
        str(duration),
        "-i",
        str(right_image),
        "-filter_complex",
        filter_complex,
        "-map",
        "[out]",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(output),
        "-y",
    ]

    print(f"Creating side-by-side video {output} from {left_image} and {right_image}")
    subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )


def overlay_audio(input_mp4_file: Path, input_mp3_file: Path):
    # Make tmp dir
    tmpdir = Path.cwd() / ".tmp" / "overlay_audio"
    tmpdir.mkdir(parents=True, exist_ok=True)

    # Copy to tmp dir
    tmp_input_mp4_file = input_mp4_file.rename(tmpdir / input_mp4_file.name)
    tmp_input_mp3_file = tmpdir / input_mp3_file.name
    shutil.copy2(input_mp3_file, tmp_input_mp3_file)

    cmd = [
        "ffmpeg",
        "-i",
        str(tmp_input_mp4_file),
        "-i",
        str(tmp_input_mp3_file),
        "-filter_complex",
        "[0:a][1:a]amix=inputs=2:dropout_transition=0[a]",
        "-map",
        "0:v",
        "-map",
        "[a]",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(input_mp4_file),
        "-y",
    ]
    print(f"Overlaying audio {input_mp3_file} onto {input_mp4_file}")
    # print(" ".join(cmd))
    subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    # Delete temp dir
    shutil.rmtree(tmpdir)


def image_to_video(input: Path, output: Path, duration: int = 5):
    cmd = [
        "ffmpeg",
        "-loop",
        "1",
        "-i",
        str(input),
        "-t",
        str(duration),
        "-vf",
        "setsar=1",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(output),
        "-y",
    ]
    print(f"Converting {input} to {output}")

    subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )


def run(file: Path):
    with open(file, "r") as f:
        data = yaml.safe_load(f)

        for entry in data:
            concatenate_dict = entry.get("concatenate")
            if concatenate_dict:
                audio = concatenate_dict.get("audio")
                videos = concatenate_dict.get("videos")
                videos_to_concatenate = []
                for video in videos:
                    if type(video) == str:
                        videos_to_concatenate.append(Path(video))
                    elif list(video.keys())[0] == "title-slide":
                        title.run_ffmpeg(
                            duration=video.get("duration", 5),
                            color=video.get("color", "black"),
                            title=video.get("title"),
                            subtitle=video.get("subtitle", ""),
                            output_file=video.get("output-file"),
                        )
                        videos_to_concatenate.append(Path(video.get("output-file")))
                    elif list(video.keys())[0] == "image-to-video":
                        image_to_video(
                            duration=video.get("duration", 5),
                            input=video.get("input"),
                            output=video.get("output"),
                        )
                        videos_to_concatenate.append(Path(video.get("output")))
                    elif list(video.keys())[0] == "images-to-side-by-side-video":
                        images_to_side_by_side_video(
                            left_image=video.get("left-image"),
                            right_image=video.get("right-image"),
                            duration=video.get("duration", 5),
                            output=video.get("output", 5),
                        )
                        videos_to_concatenate.append(Path(video.get("output")))
                output_file = concatenate_dict.get("output-file")
                concatenate.run_from_list(videos_to_concatenate, output_file, 4)
                if audio:
                    audio_to_concatenate = []
                    for entry in audio:
                        if type(entry) == str:
                            audio_to_concatenate.append(Path(entry))
                    input_mp3 = Path(audio_to_concatenate[0])
                    overlay_audio(Path(output_file), input_mp3)


def setup_parser(parser):
    parser.description = "Process commands from a YAML file."
    parser.add_argument("file", type=str, help="Input YAML file path.")
    parser.add_argument(
        "--retain-temp", action="store_true", help="Retain temporary files."
    )
    parser.add_argument(
        "--debug", action="store_true", help="Print ffmpeg command data."
    )
    return parser


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    setup_parser(parser)
    args = parser.parse_args(args)
    run(args.file)

    # run_ffmpeg(args.duration, args.color, args.output_file, args.title, args.subtitle)


if __name__ == "__main__":
    main()
