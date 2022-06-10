import os
from glob import glob
from zipfile import ZipFile

__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"


def clean_cache():
    directory = 'cache'
    parent_dir = 'C:/Users/julia/Documents/Winc/files'
    path = os.path.join(parent_dir, directory)

    try:
        os.mkdir(path)
        print("Cache directory created")
    except FileExistsError:
        print("Directory already exists. Deleting files in directory")
        files = glob(path)
        for f in files:
            os.unlink(f)
    except FileNotFoundError:
        print("Parent directory does not exist")


def cache_zip(zip_file_path, dir_path):
    with ZipFile(zip_file_path, 'r') as zip:
        zip.printdir()

        zip.extractall(dir_path)
        print('Extracted zip file')


def cached_files():
    directory = 'C:/Users/julia/Documents/Winc/files/cache'
    files_list = os.listdir(directory)
    abs_paths = []
    for file in files_list:
        abs_file = os.path.abspath(os.path.join(directory, file))
        abs_paths.append(abs_file)

    return abs_paths


def find_password(files):
    pw = ''
    for file in files:
        with open(file, 'r') as file:
            for line in file:
                if 'password' in line:
                    pw = line.strip()
                    pw = pw[(pw.find(' ')+ 1):]
    
    return pw


if __name__ == "__main__":
    clean_cache()

    # cache_zip('C:\\Users\\julia\\Documents\\Winc\\files\\data.zip', 'C:\\Users\\julia\\Documents\\Winc\\files\\cache')
    
    # cf = cached_files()
    # # print(cf)

    # pw = find_password(cf)
    # print(pw)