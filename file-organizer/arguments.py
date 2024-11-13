"""Arguemnt parser file organizer.

Author: Vishal Gattani

Usage:
    cd iteration_tool/scripts
    python3 run.py --help
"""

import argparse
from pathlib import Path

def init_argparse() -> argparse.ArgumentParser:
    """Get arguments

    Returns:
        argparse.Namespace: a utility function for parsing command-line arguments and returns the parsed arguments as an argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(
        prog="File organizer",
        description="Organize files into directories",
        epilog="",
    )
    parser.add_argument(
        "--path",
        "-p",
        dest="path",
        required=False,
        default=None,
        help="Directory path to be organized.",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        dest="recursive",
        required=False,
        default=False,
        help="Recursively organize files.",
    )
    return parser
