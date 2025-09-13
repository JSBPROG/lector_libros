import os

def create_directories(directories: list[str]) -> None:
    """
    Creates a list of directories if they don't already exist.
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
