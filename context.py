import os
import sys


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
        with open(filepath, 'rb') as file:  # Open the file in binary mode
            # Read a small portion (1024 bytes) of the file to check for binary characters
            chunk = file.read(1024)
            # Check if the chunk contains a null byte (common in binary files)
            if b'\0' in chunk:
                return False
            # Attempt to decode the chunk using UTF-8 encoding to ensure it's text
            chunk.decode('utf-8')
            return True
    # Catch errors if decoding fails or permission is denied
    except (UnicodeDecodeError, PermissionError):
        return False


def extract_text_files(directory):
    """
    Extracts the content of text files from the specified directory and writes them to an output file.
    The output file is named <directory_name>_all_text_files.txt.

    Args:
        directory (str): The path of the directory to be scanned for text files.
    """
    # Generate the output filename based on the directory name
    output_filename = f"{os.path.basename(
        directory.rstrip(os.sep))}_all_text_files.txt"

    # Get a list of all files in the given directory, excluding the output file
    all_files = [f for f in os.listdir(directory) if os.path.isfile(
        os.path.join(directory, f)) and f != output_filename]

    # Open the output file in write mode with UTF-8 encoding, ignoring encoding errors
    with open(output_filename, 'w', encoding='utf-8', errors='ignore') as outfile:
        for filename in all_files:
            # Create the full path of the file
            filepath = os.path.join(directory, filename)
            if is_text_file(filepath):  # Check if the current file is a text file
                # Open the text file in read mode with UTF-8 encoding, ignoring errors
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                    # Write a header for the file
                    outfile.write(f"--- Contents of {filename} ---\n")
                    # Write the contents of the file to the output file
                    outfile.write(infile.read())
                    # Add spacing between the content of different files
                    outfile.write("\n\n")


# Check if the directory was passed as a command-line argument
if len(sys.argv) > 1:
    # Use the first argument as the directory name
    directory_name = sys.argv[1]
else:
    # If no argument was passed, ask the user for the directory name
    directory_name = input("Please enter the directory path: ")

# Validate the directory path
if os.path.isdir(directory_name):
    extract_text_files(directory_name)
    print(f"Text files have been extracted to '{os.path.basename(directory_name.rstrip(
        os.sep))}_all_text_files.txt' from the directory: {directory_name}")
else:
    print(f"The directory '{
          directory_name}' does not exist. Please provide a valid directory path.")
