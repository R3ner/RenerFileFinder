import os
import subprocess
import platform

def search_files(directory, keyword, search_content=False, extensions=None):
    """
    Core search logic for RenerFileFinder.
    :param directory: The root folder to start searching from.
    :param keyword: The string to look for.
    :param search_content: Boolean to enable searching inside file text.
    :param extensions: List of strings (e.g., ['.txt', '.py']) to filter content search.
    """
    results = []
    keyword_lower = keyword.lower()
    
    # Ensure extensions are in a tuple format for .endswith()
    if extensions:
        # Clean extensions (ensure they start with a dot)
        valid_exts = tuple(ext if ext.startswith('.') else f'.{ext}' for ext in extensions)
    else:
        # Fallback defaults if list is empty
        valid_exts = ('.txt', '.js', '.json', '.py', '.html', '.css', '.md')

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.normpath(os.path.join(root, file))
            
            # 1. Match by filename (always checked)
            if keyword_lower in file.lower():
                results.append(file_path)
                continue # Skip content search if name already matched
            
            # 2. Match by content (only if requested and extension matches)
            if search_content and file.lower().endswith(valid_exts):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        # We read line by line for better memory management on large files
                        for line in f:
                            if keyword_lower in line.lower():
                                results.append(file_path)
                                break 
                except Exception:
                    # Skip files that can't be read (permissions, locked, etc.)
                    continue
                    
    return results

def open_file_explorer(path):
    """Opens the file explorer at the specific file location."""
    # If it's a file, we want the folder containing it
    folder = os.path.dirname(path) if os.path.isfile(path) else path
    
    if not os.path.exists(folder):
        return

    system = platform.system()
    if system == "Windows":
        os.startfile(folder)
    elif system == "Darwin":  # macOS
        subprocess.Popen(["open", folder])
    else:  # Linux
        subprocess.Popen(["xdg-open", folder])