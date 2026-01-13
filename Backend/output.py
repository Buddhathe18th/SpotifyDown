import zipfile
import os
from pathlib import Path

def zip_directory(directory_path, output_filename):
    print("\n"*4)
    print(directory_path)
    print(list(os.walk(directory_path)))
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Add file to zip with relative path
                arcname = os.path.relpath(file_path, directory_path)
                zip_file.write(file_path, arcname)
    return output_filename
