# LLM Local Context - Text File Extractor for Project Context

Wish you had a quick way to give your friendly LLM full context for all the files you are working with?
Are you packaging up your project code as zip files and uploading to your LLM? Eew!
Tired of waiting for GitHub Copilot to have true project-wide context? Look no more!!

This script extracts the contents of all text-based files in a given directory and consolidates them into a single file (`<directory>_all_text_files.txt`) and your local clipboard. This is particularly useful when working with large projects and you want to provide project context to a Language Learning Model (LLM) without needing to upload an entire ZIP archive of the project files.

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

- **Binary Detection:** Skips binary files by checking for null bytes and decoding errors.
- **UTF-8 Support:** Handles UTF-8 encoded files and ignores encoding errors where necessary.
- **Error Handling:** Catches permission and decoding errors gracefully.
- **Single Output File:** All text file contents are neatly organized in `all_text_files.txt` for easy processing.

## Installation

1. Clone or download this repository.
2. Ensure Python is installed (version 3.x is recommended).

# Environment

```bash
python3 -m venv venv
source venv/bin/activate
```
