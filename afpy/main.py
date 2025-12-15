import sys
import argparse

try:
    from ffmpeg import title
    from ffmpeg import concatenate
    from ffmpeg import from_yaml
except:
    from .ffmpeg import title
    from .ffmpeg import concatenate
    from .ffmpeg import from_yaml


def main():
    parser = argparse.ArgumentParser(description="Dispatcher for utility scripts.")

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Command to run"
    )

    title_parser = subparsers.add_parser("title", help="Generate a title slide.")
    title.setup_parser(title_parser)

    concatenate_parser = subparsers.add_parser(
        "concatenate", help="Generate a title slide."
    )
    concatenate.setup_parser(concatenate_parser)

    yaml_parser = subparsers.add_parser("yaml", help="Generate a title slide.")
    from_yaml.setup_parser(yaml_parser)

    # Parse known args to avoid argparse errors for forwarding
    args, remaining_args = parser.parse_known_args()

    # Forward remaining args to the selected module
    if args.command == "title":
        title.main(sys.argv[2:])
    elif args.command == "concatenate":
        concatenate.main(sys.argv[2:])
    elif args.command == "yaml":
        from_yaml.main(sys.argv[2:])


if __name__ == "__main__":
    main()
