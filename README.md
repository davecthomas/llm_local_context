# LLM Local Context - Text File Extractor for Project Context

Wish you had a quick way to give your friendly LLM full context for all the files you are working with?
Are you packaging up your project code as zip files and uploading to your LLM? Eew!
Tired of waiting for GitHub Copilot to have true project-wide context? Look no more!!

This script recursively scans and extracts the contents of all text-based files in a given directory tree and consolidates them into a single file (`<directory>_all_text_files.txt`) and your local clipboard. This is particularly useful when working with large projects and you want to provide project context to a Language Learning Model (LLM) without needing to upload an entire ZIP archive of the project files.

## Typical Scenario

You have updated your project code a ton and have a big new question to present to your favorite LLM. Use this tool to grab all the code into your clipboard and them prompt the LLM with "Here's my current code. Analyze it and then I'll have a big new feature to add with you..." (then you paste the contents and go!)

## Input

The script accepts the directory path in two ways:

1. **Command-line argument:** You can pass the directory path as a parameter when running the script.
   Example:
   ```bash
   python context.py /path/to/your/directory
   ```

## How It Works

- The script checks each file in the directory to determine if it's a text file.
- Binary files (or files that can't be decoded as UTF-8) are automatically skipped.
- The contents of all text files are concatenated and written to `all_text_files.txt` in a readable format, with clear separation between the content of each file. It is also dropped into your clipboard.

## Use Case

When you want to provide project context to an LLM (such as OpenAI's GPT) for code analysis, review, or question-answering, this script helps by creating a consolidated view of all relevant text files. By doing this, you can avoid the need to upload ZIP archives or multiple files.

## Features

- **Exclude Files:** Uses the same approach as .gitignore to make it easy to just copy that over as `exclude.files`.
- **Binary Detection:** Skips binary files by checking for null bytes and decoding errors.
- **UTF-8 Support:** Handles UTF-8 encoded files and ignores encoding errors where necessary.
- **Error Handling:** Catches permission and decoding errors gracefully.
- **Single Output File:** All text file contents are neatly organized in `all_text_files.txt` for easy processing.

### Excluding Files and Directories

This tool leverages an exclusion mechanism to filter out files and directories that you don't want to include in the consolidated output. The exclusion patterns are specified in an `exclude.files` file located in the project root (or a specified path).

### How It Works

- **Loading Exclusion Patterns:**  
  The script reads the `exclude.files` file line by line using the `load_excluded_patterns()` function.

  - Blank lines and lines starting with `#` (comments) are ignored.
  - Each non-comment line is treated as a pattern.
  - Works just like .gitignore

- **Pattern Matching:**  
  The patterns support Unix shell-style wildcards (e.g., `*.log`, `*.pyc`) and can target directories by including a trailing slash (e.g., `venv/`, `__pycache__/`).  
  These patterns are applied using Python's `fnmatch` module to determine if a file or directory should be excluded.

- **Application During Scanning:**  
  During the recursive directory traversal:
  - Directories that match any exclusion pattern are skipped, preventing further recursion into them.
  - Files that match any pattern are ignored, ensuring that only relevant text-based files are included.

### Example `exclude.files`

````text
.git
# Log files
*.log
*.log.*
*.pyc
__pycache__/
venv/
# Ignore configuration files
.config


## Installation

1. Clone or download this repository.
2. Ensure Python is installed (version 3.x is recommended).

# Environment

```bash
python3 -m venv venv
source venv/bin/activate
````
