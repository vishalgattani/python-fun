from pathlib import Path
import shutil
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_file_size(file_path: Path) -> int:
    """Get file size.

    Args:
        file_path (Path): File path.

    Returns:
        int: Size in bytes.
    """
    return file_path.stat().st_size

def collect_files(path: Path, pattern:str = "*.*", recursive: bool = False) -> list:
    """Collect files from a directory.

    Args:
        path (Path): Directory path.
        pattern (str): Pattern to match files.
        recursive (bool, optional): Recursively collect files. Defaults to False.

    Returns:
        list: List of files matching the pattern.
    """
    if recursive:
        return list(path.rglob(pattern))
    else:
        return list(path.glob(pattern))

def is_compressed(file_path: Path) -> bool:
    """Check if a file is compressed.

    Args:
        file_path (Path): Path to the file.

    Returns:
        bool: True if the file is compressed, False otherwise.
    """
    return file_path.suffix in (".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz")

def is_audio(file_path: Path) -> bool:
    """Check if a file is an audio file.

    Args:
        file_path (Path): Path to the file.

    Returns:
        bool: True if the file is an audio file, False otherwise.
    """
    return file_path.suffix in (".3ga", ".aac", ".ac3", ".aif", ".aiff",
         ".alac", ".amr", ".ape", ".au", ".dss",
         ".flac", ".flv", ".m4a", ".m4b", ".m4p",
         ".mp3", ".mpga", ".ogg", ".oga", ".mogg",
         ".opus", ".qcp", ".tta", ".voc", ".wav",
         ".wma", ".wv", ".mpeg")

def is_pkg(file_path: Path) -> bool:
    """Check if a file is a package.

    Args:
        file_path (Path): Path to the file.

    Returns:
        bool: True if the file is a package, False otherwise.
    """
    return file_path.suffix in (".apk", ".ipa", ".deb", ".rpm", ".jar", ".exe", ".msi", ".pkg")

def is_dmg(file_path: Path) -> bool:
    """Check if a file is a dmg file.

    Args:
        file_path (Path): Path to the file.

    Returns:
        bool: True if the file is a dmg file, False otherwise.
    """
    return file_path.suffix in (".dmg")

def is_image(file_path: Path) -> bool:
    """Check if a file is an image file.

    Args:
        file_path (Path): Path to the file.

    Returns:
        bool: True if the file is an image file, False otherwise.
    """
    return file_path.suffix in (".bmp", ".gif", ".jpg", ".jpeg", ".png", ".psd", ".svg", ".tif", ".tiff")

def is_screenshot(file_path: Path) -> bool:
    """Check if a file is a screenshot.

    Args:
        file_path (Path): Path to the file.

    Returns:
        bool: True if the file is a screenshot, False otherwise.
    """
    return is_image(file_path) and "screenshot" in file_path.name.lower()

def is_document(file_path: Path) -> bool:
    """Check if a file is a document.

    Args:
        file_path (Path): Path to the file.

    Returns:
        bool: True if the file is a document, False otherwise.
    """
    return file_path.suffix in (".doc", ".docx", ".odt", ".pdf", ".rtf", ".tex", ".txt", ".wpd")

def is_video(file_path: Path) -> bool:
    """Check if a file is a video file.

    Args:
        file_path (Path): Path to the file.

    Returns:
        bool: True if the file is a video file, False otherwise.
    """
    return file_path.suffix in (".webm", ".MTS", ".M2TS", ".TS", ".mov",
         ".mp4", ".m4p", ".m4v", ".mxf")

def move_file(file_path: Path, destination: Path) -> None:
    """Move a file to a destination.

    Args:
        file_path (Path): Path to the file.
        destination (Path): Path to the destination.
    """
    destination.mkdir(parents=True, exist_ok=True)
    try:
        assert destination.is_dir(), f"Destination {destination} is not a directory."
        assert file_path.is_file(), f"{file_path} is not a file."
        assert file_path.exists(), f"{file_path} does not exist."
        assert destination.exists(), f"{destination} does not exist."
        shutil.move(src=str(file_path.resolve()), dst=str(destination.resolve()))
    except AssertionError as e:
        logger.error(e)
    except shutil.Error as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
        logger.exception("Unexpected error occurred.")

def organize_files(directory_to_scan: Path, recursive:bool = False) -> None:
    """Organize files in a directory.

    Args:
        directory_to_scan (Path): Path to the directory.
        recursive (bool, optional): Whether to recursively scan the directory. Defaults to False.
    """
    all_files = collect_files(path=directory_to_scan, recursive=recursive)
    for file in all_files:
        if is_audio(file_path=file):
            move_file(file_path=file, destination=directory_to_scan/"audios")
        elif is_image(file_path=file):
            if is_screenshot(file_path=file):
                move_file(file_path=file, destination=directory_to_scan/"screenshots")
            else:
                move_file(file_path=file, destination=directory_to_scan/"images")
        elif is_video(file_path=file):
            move_file(file_path=file, destination=directory_to_scan/"videos")
        elif is_document(file_path=file):
            move_file(file_path=file, destination=directory_to_scan/"docs")
        elif is_pkg(file_path=file):
            move_file(file_path=file, destination=directory_to_scan/"pkgs")
        elif is_dmg(file_path=file):
            move_file(file_path=file, destination=directory_to_scan/"dmg")
        elif is_compressed(file_path=file):
            move_file(file_path=file, destination=directory_to_scan/"compressed")
        else:
            logger.warning(f"Skipping {file}")