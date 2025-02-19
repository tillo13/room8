import os
from datetime import datetime

# Boolean flags to control whether to include HTML, JS, CSS, and Markdown files
INCLUDE_HTML = True
INCLUDE_JS = True
INCLUDE_CSS = True
INCLUDE_MD = True

# Global variable to define directories to exclude from scanning
# Note: "directory_printouts" is added so that the generated file doesn’t get scanned.
DIRECTORIES_TO_EXCLUDE = [".git", "directory_printouts", "VERSIONS", "__pycache__", "othersecretefolder"]

# Global variable to define directories to completely exclude from the final output file
DIRECTORIES_MAP_TO_EXCLUDE = [".git", "directory_printouts", "VERSIONS", "__pycache__"]

def gather_files(root_dir, directories_to_exclude, directories_map_to_exclude, include_html, include_js, include_css, include_md):
    """
    Gathers all .py files (and optionally .html, .js, .css, and .md files) within the specified root directory
    and its subdirectories, excluding specified directories and ignoring the gather_pythons.py file.

    Parameters:
        root_dir (str): The root directory to search for files.
        directories_to_exclude (list): Directory names to exclude from scanning.
        directories_map_to_exclude (list): Directory names to completely exclude from output.
        include_html (bool): Whether to include HTML files.
        include_js (bool): Whether to include JS files.
        include_css (bool): Whether to include CSS files.
        include_md (bool): Whether to include Markdown files.
    
    Returns:
        tuple: (files, directories, excluded_directories)
            files: list of tuples (filepath, file_contents)
            directories: sorted list of directories found
            excluded_directories: sorted list of directories that were excluded
    """
    files = []
    directories = set()
    excluded_directories = set()

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Get the relative path from the root directory.
        relative_path = os.path.relpath(dirpath, root_dir)
        # Use split to break the path into directories and check if any part should be excluded.
        if any(excluded in relative_path.split(os.sep) for excluded in directories_to_exclude + directories_map_to_exclude):
            excluded_directories.add(relative_path)
            continue

        directories.add(relative_path)
        
        for filename in filenames:
            # Skip the script file itself
            if filename == "gather_pythons.py":
                continue

            # Check file extension and add the file if it matches the criteria.
            if (filename.endswith('.py') or 
                (include_html and filename.endswith('.html')) or 
                (include_js and filename.endswith('.js')) or 
                (include_css and filename.endswith('.css')) or 
                (include_md and filename.endswith('.md'))):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        file_contents = file.read()
                    files.append((filepath, file_contents))
                except UnicodeDecodeError:
                    print(f"Could not read file {filepath} due to encoding error. Skipping.")
                except Exception as e:
                    print(f"An unexpected error occurred with file {filepath}: {e}")

    return files, sorted(directories), sorted(excluded_directories)

def write_to_file(output_filepath, data, directories, excluded_directories, directories_map_to_exclude):
    """
    Writes the gathered data to a file with counts of files and directories,
    the directory structure, followed by a list of all file paths and their contents.

    Parameters:
        output_filepath (str): Path of the file where data will be written.
        data (list): List of tuples (filepath, file_content).
        directories (list): Sorted list of directories containing files.
        excluded_directories (list): Sorted list of directories that were excluded.
        directories_map_to_exclude (list): Directory names to exclude from final output.
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
    root_dir = "."  # Change this if needed; by default, it uses the current directory.

    # Ensure the output directory exists.
    output_dir = "directory_printouts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a timestamped filename and place it into the output directory.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filepath = os.path.join(output_dir, f"{timestamp}_files_within.txt")
    
    # Gather files and directories.
    files, directories, excluded_directories = gather_files(
        root_dir,
        DIRECTORIES_TO_EXCLUDE,
        DIRECTORIES_MAP_TO_EXCLUDE,
        INCLUDE_HTML,
        INCLUDE_JS,
        INCLUDE_CSS,
        INCLUDE_MD  # Pass the Markdown inclusion flag
    )
    
    # Write the results to the output file.
    write_to_file(output_filepath, files, directories, excluded_directories, DIRECTORIES_MAP_TO_EXCLUDE)
    print(f"Files have been gathered and written to {output_filepath}")

if __name__ == "__main__":
    main()