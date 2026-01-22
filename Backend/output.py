import zipfile
import os
from pathlib import Path

def zip_directory(directory_path, output_filename):
    directory_path = os.path.abspath(directory_path)
    output_filename = os.path.abspath(output_filename)

    print("\n"*4)
    print(f"Directory to zip: {directory_path}")
    print(f"Directory exists: {os.path.exists(directory_path)}")
    print(f"Files found: {list(os.walk(directory_path))}")

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)


    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Add file to zip with relative path
                arcname = os.path.relpath(file_path, directory_path)
                print(f"Adding to zip: {file_path} as {arcname}")
                zip_file.write(file_path, arcname)
    
    return output_filename
