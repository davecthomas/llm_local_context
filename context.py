import os
import sys
import platform
import subprocess
import fnmatch


def load_excluded_patterns(filepath="excluded.files"):
    """
    Loads file patterns to be excluded from the exclude files.

    Args:
        filepath (str): The path to the exclude files.

    Returns:
        list: A list of patterns to be excluded.
    """
    excluded_patterns = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as exclude_file:
            for line in exclude_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    excluded_patterns.append(line)
    return excluded_patterns


def is_text_file(filepath):
    """
    Determines if a given file is a text file by checking for the presence of binary characters
    and attempting to decode the file's contents using UTF-8 encoding.

    Args:
        filepath (str): The path of the file to be checked.

    Returns:
        bool: True if the file is a text file, False otherwise.
    """
    try:
        with open(filepath, 'rb') as file:
            # Read a small portion (1024 bytes) of the file to check for binary characters
            chunk = file.read(1024)
            # Check if the chunk contains a null byte (common in binary files)
            if b'\0' in chunk:
                return False
            # Attempt to decode the chunk using UTF-8 encoding to ensure it's text
            chunk.decode('utf-8')
            return True
    except (UnicodeDecodeError, PermissionError):
        return False


def should_exclude(path, excluded_patterns):
    """
    Checks if a given path matches any of the excluded patterns.

    Args:
        path (str): The path to be checked.
        excluded_patterns (list): The list of patterns to exclude.

    Returns:
        bool: True if the path should be excluded, False otherwise.
    """
    for pattern in excluded_patterns:
        # Normalize pattern for directory matching
        normalized_pattern = pattern.rstrip('/')
        if fnmatch.fnmatch(path, normalized_pattern) or fnmatch.fnmatch(os.path.basename(path), normalized_pattern):
            return True
    return False


def extract_text_files(directory, excluded_patterns):
    """
    Extracts the content of text files from the specified directory and writes them to an output file.
    Stops after reading 10,000 lines to avoid unnecessary processing.

    Args:
        directory (str): The path of the directory to be scanned for text files.
        excluded_patterns (list): A list of patterns to exclude.
    """
    # Generate the output filename based on the directory name
    output_filename = f"{os.path.basename(
        directory.rstrip(os.sep))}_all_text_files.txt"

    max_lines = 10000  # Limit to 10K lines
    line_count = 0

    # Open the output file in write mode with UTF-8 encoding, ignoring encoding errors
    with open(output_filename, 'w', encoding='utf-8', errors='ignore') as outfile:
        # Walk through the directory tree
        for root, dirs, files in os.walk(directory):
            # Exclude directories based on patterns
            dirs[:] = [d for d in dirs if not should_exclude(
                os.path.join(root, d), excluded_patterns)]

            for filename in files:
                filepath = os.path.join(root, filename)
                # Skip the output file itself
                if os.path.abspath(filepath) == os.path.abspath(output_filename):
                    continue
                # Exclude files based on patterns
                if should_exclude(filepath, excluded_patterns):
                    continue
                if is_text_file(filepath):
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                        outfile.write(f"--- Contents of {filepath} ---\n")
                        for line in infile:
                            outfile.write(line)
                            line_count += 1
                            if line_count >= max_lines:
                                print(f"Reached the limit of {
                                      max_lines} lines. Exiting.")
                                outfile.write("\n\n")
                                # Copy to clipboard before exiting
                                copy_to_clipboard(output_filename)
                                return
                        outfile.write("\n\n")

    # Copy the output file to the clipboard on macOS
    copy_to_clipboard(output_filename)


def copy_to_clipboard(output_filename):
    """
    Copies the content of the output file to the clipboard on macOS.

    Args:
        output_filename (str): The path to the output file.
    """
    if platform.system() == "Darwin":
        with open(output_filename, 'r', encoding='utf-8', errors='ignore') as output_file:
            content = output_file.read()
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(content.encode('utf-8'))
        print(f"The content of '{
              output_filename}' has been copied to the clipboard.")


# Main execution
if __name__ == "__main__":
    # Check if the directory was passed as a command-line argument
    if len(sys.argv) > 1:
        directory_name = sys.argv[1]
    else:
        directory_name = input("Please enter the directory path: ")

    # Validate the directory path
    if os.path.isdir(directory_name):
        # Load excluded patterns from excluded.files
        excluded_patterns = load_excluded_patterns("exclude.files")
        extract_text_files(directory_name, excluded_patterns)
        print(f"Text files have been extracted to '{os.path.basename(directory_name.rstrip(
            os.sep))}_all_text_files.txt' from the directory: {directory_name}")
    else:
        print(f"The directory '{
              directory_name}' does not exist. Please provide a valid directory path.")
