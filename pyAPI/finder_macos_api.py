import subprocess
from pathlib import Path

from flask import Flask, jsonify, request


class FileSearchAPP:
    def __init__(self):
        self.app = Flask(__name__)
        self.base_directory = str(Path.home().resolve())
        self.threshold_sizes = {"MB": 1024 * 1024, "KB": 1024}
        self._register_routes()

    def _register_routes(self):
        """Setting up endpoints"""
        self.app.add_url_rule("/search", "find_files", self.find_files, methods=["GET"])
        self.app.add_url_rule(
            "/find", "find_directories", self.find_directories, methods=["GET"]
        )
        self.app.add_url_rule(
            "/list", "get_file_sizes", self.get_file_sizes, methods=["GET"]
        )
        self.app.add_url_rule(
            "/listdir", "get_directory_size", self.get_directory_size, methods=["GET"]
        )
        self.app.add_url_rule(
            "/filter_dir", "filter_directory", self.filter_directory, methods=["GET"]
        )
        self.app.add_url_rule(
            "/filter_files", "filter_files", self.filter_files, methods=["GET"]
        )

    def find_files(self):
        file_pattern = request.args.get("filename")
        recursive = request.args.get("recursive", False)
        search_directory = request.args.get("directory", self.base_directory)
        if not file_pattern:
            return jsonify({"error": "Filename or pattern is required"}), 400
        if recursive:
            files = [
                str(x.resolve())
                for x in list(Path(search_directory).rglob(file_pattern))
                if x.is_file()
            ]
        else:
            files = [
                str(x.resolve())
                for x in list(Path(search_directory).rglob(file_pattern))
                if x.is_file()
            ]
        if files:
            return jsonify({"message": "File(s) found", "files": files}), 200
        else:
            return jsonify({"message": "File(s) not found", "files": []})

    def find_directories(self):
        directory = request.args.get("directory")
        recursive = request.args.get("recursive", False)
        if not directory:
            return jsonify({"error": "Directory name is required"})
        if not Path(directory).exists():
            return jsonify({"error": f"Directory {directory} does not exist"})
        if recursive:
            dirs = [
                str(x.resolve())
                for x in list(Path(self.base_directory).rglob(directory))
                if x.is_dir()
            ]
        else:
            dirs = [
                str(x.resolve())
                for x in list(Path(self.base_directory).glob(directory))
                if x.is_dir()
            ]
        if dirs:
            return jsonify({"message": "Directory found", "directories": dirs}), 200
        else:
            return jsonify({"message": "Directory not found", "directories": []})

    def get_file_sizes(self):
        directory = request.args.get("directory")
        if not directory:
            return jsonify({"error": "Directory name is required"})
        files = {
            str(file): self._get_file_size(file)
            for file in list(Path(directory).glob("*"))
            if file.is_file()
        }
        return jsonify({"file_sizes": files})

    def _get_file_size(self, file):
        return file.stat().st_size

    def _get_dir_size(self, path):
        process = subprocess.run(
            ["du", "-s", "-b", str(path)],  # Use a list for command arguments
            capture_output=True,  # Capture standard output and error
            text=True,  # Return output as a string (not bytes)
        )
        return process.stdout.strip().split()[0]

    def get_directory_size(self):
        directory = request.args.get("directory")
        if not directory:
            return jsonify({"error": "Directory name is required"})
        if not Path(directory).exists():
            return jsonify({"error": f"Directory {directory} does not exist"})
        dirs = {
            str(dirs): self._get_dir_size(dirs.resolve())
            for dirs in list(Path(directory).glob("*"))
            if dirs.is_dir()
        }
        return jsonify({"directory_name": dirs}), 200

    def filter_files(self):
        size_threshold_bytes = int(
            request.args.get("threshold", self.threshold_sizes["MB"])
        )
        directory = request.args.get("directory")
        file_name = request.args.get("filename", None)
        if not directory:
            return jsonify({"error": "Directory name is required"})
        if not Path(directory).exists():
            return jsonify({"error": f"Directory {directory} does not exist"})

        files = {
            str(file): self._get_file_size(file)
            for file in list(
                Path(directory).glob(pattern=f"*{file_name}*" if file_name else "*")
            )
            if (file.is_file() and self._get_file_size(file) < size_threshold_bytes)
        }
        return (
            jsonify(
                {
                    "file_sizes": {
                        "search_directory": directory,
                        "files": files,
                        "threshold": size_threshold_bytes,
                    }
                }
            ),
            200,
        )

    def filter_directory(self):
        size_threshold_bytes = int(
            request.args.get("threshold", self.threshold_sizes["MB"])
        )
        directory = request.args.get("directory")
        if not directory:
            return jsonify({"error": "Directory name is required"})
        if not Path(directory).exists():
            return jsonify({"error": f"Directory {directory} does not exist"})

        dirs = {
            str(dirs): self._get_dir_size(dirs.resolve())
            for dirs in list(Path(directory).glob(pattern="*"))
            if (
                dirs.is_dir()
                and self._get_dir_size(dirs.resolve()) < size_threshold_bytes
            )
        }
        return (
            jsonify(
                {
                    "directory_sizes": {
                        "directories": dirs,
                        "threshold": size_threshold_bytes,
                    }
                }
            ),
            200,
        )

    def run(self):
        """Run the Flask application."""
        self.app.run(debug=True)


def main():
    app_instance = FileSearchAPP()
    app_instance.run()


if __name__ == "__main__":
    main()
