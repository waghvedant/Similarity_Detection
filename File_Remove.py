import os

def remove_out_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".out"):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f"Removed: {file_path}")

