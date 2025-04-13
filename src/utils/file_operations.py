"""
File and directory management utility functions for the Python CLI AI Coder.

This module provides a set of utility functions for file and directory operations
that are used by the project generator. These functions handle common tasks such as:
- Reading and writing files
- Getting file metadata
- Listing directory contents
- Creating directories
- Path safety validation

All functions include safety checks to ensure operations are restricted to the
current working directory for security.
"""
import os
import datetime
import stat
from pathlib import Path


def is_safe_path(path):
    """
    Validates if the path is within current working directory.

    Args:
        path (str): Path to validate

    Returns:
        bool: True if path is safe, False otherwise
    """
    # Get absolute paths for comparison
    path = os.path.abspath(path)
    cwd = os.path.abspath(os.getcwd())

    # Check if the path is within the current working directory
    return path.startswith(cwd)


def read_file(filename):
    """
    Reads and returns the contents of a file in the current working directory.

    Args:
        filename (str): Name of the file to read

    Returns:
        str: Contents of the file if successful
        None: If file doesn't exist or isn't in the current directory
    """
    if not is_safe_path(filename):
        print(f"Error: File '{filename}' is not in the current working directory.")
        return None

    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def get_file_metadata(filename):
    """
    Returns metadata for a file in the current working directory.

    Args:
        filename (str): Name of the file to get metadata for

    Returns:
        dict: Dictionary containing file metadata if successful
        None: If file doesn't exist or isn't in the current directory
    """
    if not is_safe_path(filename):
        print(f"Error: File '{filename}' is not in the current working directory.")
        return None

    try:
        file_path = Path(filename)
        if not file_path.exists():
            print(f"Error: File '{filename}' not found.")
            return None

        stat_info = file_path.stat()

        # Convert timestamps to human-readable format
        created_time = datetime.datetime.fromtimestamp(stat_info.st_ctime)
        modified_time = datetime.datetime.fromtimestamp(stat_info.st_mtime)
        accessed_time = datetime.datetime.fromtimestamp(stat_info.st_atime)

        # Get file permissions
        perms = stat.filemode(stat_info.st_mode)

        metadata = {
            'name': file_path.name,
            'size': stat_info.st_size,  # Size in bytes
            'created': created_time,
            'modified': modified_time,
            'accessed': accessed_time,
            'permissions': perms,
            'is_directory': file_path.is_dir(),
            'is_file': file_path.is_file(),
            'absolute_path': file_path.absolute(),
        }

        return metadata
    except Exception as e:
        print(f"Error getting file metadata: {e}")
        return None


def list_directory_contents(directory="."):
    """
    Lists all files and directories in the specified directory.

    Args:
        directory (str): Directory to list contents from (defaults to current directory)

    Returns:
        dict: Dictionary with 'files' and 'directories' lists if successful
        None: If directory doesn't exist or isn't in the current working directory
    """
    if not is_safe_path(directory):
        print(f"Error: Directory '{directory}' is not in the current working directory.")
        return None

    try:
        # Get the absolute path of the directory
        abs_dir = os.path.abspath(directory)

        if not os.path.exists(abs_dir):
            print(f"Error: Directory '{directory}' not found.")
            return None

        if not os.path.isdir(abs_dir):
            print(f"Error: '{directory}' is not a directory.")
            return None

        # Lists to store files and directories
        files = []
        directories = []

        # Iterate through directory contents
        for item in os.listdir(abs_dir):
            item_path = os.path.join(abs_dir, item)
            if os.path.isfile(item_path):
                files.append(item)
            elif os.path.isdir(item_path):
                directories.append(item)

        return {
            'files': files,
            'directories': directories,
            'total_files': len(files),
            'total_directories': len(directories)
        }
    except Exception as e:
        print(f"Error listing directory contents: {e}")
        return None


def write_to_file(filename, content, mode="w"):
    """
    Writes content to a file in the current working directory.

    Args:
        filename (str): Name of the file to write to
        content (str): Content to write to the file
        mode (str): Write mode ('w' for overwrite, 'a' for append)

    Returns:
        bool: True if writing was successful, False otherwise
    """
    if not is_safe_path(filename):
        print(f"Error: File '{filename}' is not in the current working directory.")
        return False

    try:
        # Create directories if they don't exist
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, mode) as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False


def create_directory(directory_name):
    """
    Creates a directory in the current working directory.

    Args:
        directory_name (str): Name of directory to create

    Returns:
        bool: True if creation was successful, False otherwise
    """
    if not is_safe_path(directory_name):
        print(f"Error: Directory '{directory_name}' is not in the current working directory.")
        return False

    try:
        # Create the directory
        os.makedirs(directory_name, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")
        return False
