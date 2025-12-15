import subprocess, sys, argparse, shutil, time, glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def run(cmd):
    subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )


def ensure_tmp_dir(base):
    tmp = base / ".tmp" / "concatenate"
    tmp.mkdir(parents=True, exist_ok=True)
    return tmp


def collect_inputs(pattern):
    paths = sorted(Path(p) for p in glob.glob(pattern))
    if not paths:
        raise RuntimeError("No input files matched.")
    return paths


def normalize_single(p, out_dir):
    out = out_dir / p.name

    # Probe input for audio
    has_audio = False
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "a",
                "-show_entries",
                "stream=index",
                "-of",
                "csv=p=0",
                str(p),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        has_audio = bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        has_audio = False

    if has_audio:
        # Normal case: re-encode video and audio
        cmd = [
            "ffmpeg",
            "-i",
            str(p),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-profile:v",
            "high",
            "-level",
            "4.0",
            "-r",
            "30",
            "-fps_mode",
            "cfr",
            "-fflags",
            "+genpts",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(out),
            "-y",
        ]
    else:
        # Add silent audio: two inputs, map video and audio
        cmd = [
            "ffmpeg",
            "-i",
            str(p),
            "-f",
            "lavfi",
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-profile:v",
            "high",
            "-level",
            "4.0",
            "-r",
            "30",
            "-fps_mode",
            "cfr",
            "-fflags",
            "+genpts",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-shortest",
            str(out),
            "-y",
        ]

    run(cmd)
    return out


def normalize_timestamps(files, out_dir, workers=16):
    normalized = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(normalize_single, f, out_dir) for f in files]
        for future in futures:
            normalized.append(future.result())
    return normalized


def write_concat_list(files, list_path):
    with list_path.open("w", encoding="utf-8") as f:
        for p in files:
            f.write(f"file '{p.as_posix()}'\n")


def concat(list_path, output):
    cmd = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_path),
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        str(output),
        "-y",
    ]
    run(cmd)


def setup_parser(parser):
    parser.description = "Concatenate videos with timestamp normalization (parallel)."
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input-glob", help="Glob pattern for input files")
    group.add_argument(
        "--input-list",
        help="Path to file containing newline separated list of files to concatenate",
    )
    parser.add_argument(
        "--output", default=None, help="Output file (default: output<TIMESTAMP>.mp4)."
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="Number of parallel ffmpeg jobs."
    )
    return parser


def run_from_glob(input_glob, output, workers):
    input_list = collect_inputs(input_glob)
    run_from_list(input_list, output, workers)


def run_from_list(input_list: list[Path], output, workers):

    tmp = ensure_tmp_dir(Path.cwd())

    normalized = normalize_timestamps(input_list, tmp, workers=workers)

    list_path = tmp / "list.txt"
    write_concat_list(normalized, list_path)

    concat(list_path, tmp / output)
    normalize_timestamps([tmp / output], Path.cwd())

    shutil.rmtree(tmp)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    setup_parser(parser)
    args = parser.parse_args(args)
    if args.output:
        output = Path(args.output)
    else:
        ts = int(time.time())
        output = Path.cwd() / f"output{ts}.mp4"
    if args.input_glob:
        run_from_glob(args.input_glob, output, args.workers)
    else:  # args.input_list
        run_from_list(args.input_list, output, args.workers)


if __name__ == "__main__":
    main()
