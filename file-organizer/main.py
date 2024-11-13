from pathlib import Path
import arguments
import logging
import utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    parser = arguments.init_argparse()
    args = parser.parse_args()
    directory_to_scan = Path("/Users/vishalgattani/Downloads") if not args.path else Path(args.path)
    logger.info(f"Scanning directory: {directory_to_scan}")
    utils.organize_files(directory_to_scan=directory_to_scan,recursive=args.recursive)

if __name__ == "__main__":
    main()