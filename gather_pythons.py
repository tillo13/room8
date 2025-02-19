import os
from datetime import datetime

# Boolean flags to control whether to include HTML, JS, and CSS files
INCLUDE_HTML = True
INCLUDE_JS = True
INCLUDE_CSS = True

# Global variable to define directories to exclude from scanning
DIRECTORIES_TO_EXCLUDE = ["VERSIONS", "__pycache__", "pets_venv", "ip_adapter", "2024sept7_test", "othersecretefolder"]

# Global variable to define directories to completely exclude from the final output file
DIRECTORIES_MAP_TO_EXCLUDE = ["VERSIONS", "__pycache__", "pets_venv"]

def gather_files(root_dir, directories_to_exclude, directories_map_to_exclude, include_html, include_js, include_css):
    """
    Gathers all .py files (and optionally .html, .js, and .css files) within the specified root directory
    and its subdirectories, excluding specified directories and ignoring the gather_pythons.py file.

    Parameters:
        root_dir (str): The root directory to search for files.
        directories_to_exclude (list): List of directory names to exclude from scanning.
        directories_map_to_exclude (list): List of directory names to completely exclude from both scanning and output file.
        include_html (bool): Whether to include HTML files.
        include_js (bool): Whether to include JS files.
        include_css (bool): Whether to include CSS files.

    Returns:
        tuple: A tuple containing:
            - List of tuples (filepath, file_contents).
            - Sorted list of directories found.
            - Sorted list of directories excluded.
    """
    files = []
    directories = set()
    excluded_directories = set()

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the directory should be excluded
        relative_path = os.path.relpath(dirpath, root_dir)
        if any(excluded_dir in relative_path.split(os.sep) for excluded_dir in directories_to_exclude + directories_map_to_exclude):
            excluded_directories.add(relative_path)
            continue

        directories.add(relative_path)
        
        for filename in filenames:
            # Skip the file that runs this script
            if filename == "gather_pythons.py":
                continue

            # Check file extension
            if filename.endswith('.py') \
               or (include_html and filename.endswith('.html')) \
               or (include_js and filename.endswith('.js')) \
               or (include_css and filename.endswith('.css')):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        file_contents = file.read()
                    files.append((filepath, file_contents))
                except UnicodeDecodeError:
                    print(f"Could not read file {filepath} due to encoding error. Skipping this file.")
                except Exception as e:
                    print(f"An unexpected error occurred with file {filepath}: {e}")

    return files, sorted(directories), sorted(excluded_directories)

def write_to_file(output_filepath, data, directories, excluded_directories, directories_map_to_exclude):
    """
    Writes the gathered data to a file with the number of files and directories,
    the directory structure, followed by a list of all file paths and their content.

    Parameters:
        output_filepath (str): The file in which the data will be written.
        data (list of tuples): The data to write to the file. Each tuple contains (filepath, file_content).
        directories (list): The list of directories containing files.
        excluded_directories (list): The list of directories that were excluded from scanning.
        directories_map_to_exclude (list): The list of directories to exclude from the final output.
    """
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(f"Number of files: {len(data)}\n")
        file.write(f"Number of directories: {len(directories) + len(excluded_directories)}\n\n")
        
        file.write("Directory structure:\n")
        for directory in directories:
            if not any(excluded in directory for excluded in directories_map_to_exclude):
                file.write(f"{directory}\n")
        for excluded_directory in excluded_directories:
            if not any(excluded in excluded_directory for excluded in directories_map_to_exclude):
                file.write(f"{excluded_directory} [excluded from files_within.txt]\n")
        file.write("\n")
        
        file.write("List of file paths:\n")
        for filepath, _ in data:
            if not any(excluded in filepath for excluded in directories_map_to_exclude):
                file.write(f"{filepath}\n")
        file.write("\n")
        
        for filepath, file_contents in data:
            if not any(excluded in filepath for excluded in directories_map_to_exclude):
                file.write(f"{filepath}:\n{file_contents}\n")

def main():
    root_dir = "."  # Change this if your script is in a different directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filepath = f"{timestamp}_files_within.txt"
    files, directories, excluded_directories = gather_files(
        root_dir,
        DIRECTORIES_TO_EXCLUDE,
        DIRECTORIES_MAP_TO_EXCLUDE,
        INCLUDE_HTML,
        INCLUDE_JS,
        INCLUDE_CSS
    )
    write_to_file(output_filepath, files, directories, excluded_directories, DIRECTORIES_MAP_TO_EXCLUDE)
    print(f"Files have been gathered and written to {output_filepath}")

if __name__ == "__main__":
    main()