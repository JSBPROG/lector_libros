import os

def create_directories(directories: list[str]) -> None:
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
