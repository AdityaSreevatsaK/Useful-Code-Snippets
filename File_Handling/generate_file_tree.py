import os


def generate_file_tree(path, indent='~'):
    """
    Description:
        Generate and print a visual representation of the file tree for a given directory.
        This function recursively traverses the directory structure and prints the file
        and folder hierarchy in a tree-like format.

    Args:
        path (str): The root directory path for which the file tree is to be generated.
        indent (str): The indentation string used for formatting the tree structure.

    Returns:
        None
    """
    for item in sorted(os.listdir(path)):
        full_path = os.path.join(path, item)
        print(indent + '├── ' + item)
        if os.path.isdir(full_path):
            generate_file_tree(full_path, indent + '│   ')
