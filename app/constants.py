import os

input_directory = "temp_files"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_FILE_FOLDER = os.path.join(ROOT_DIR, input_directory)
os.makedirs(TEMP_FILE_FOLDER, exist_ok=True)