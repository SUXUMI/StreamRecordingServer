import os, time


def get_directory_size(directory):
    """
    Returns the directory size in bytes.
    @source: https://www.thepythoncode.com/article/get-directory-size-in-bytes-using-python
    """

    total = 0

    try:
        # Getting the directory size
        for entry in os.scandir(directory):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                total += get_directory_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    except Exception:
        return 0
    return total


def remove_empty_folders(path):
    "Removes the empty folders"
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)

    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)
            else:
                print("Removing the file:", fullpath)
                os.remove(fullpath)

    # if folder is empty, delete it
    files = os.listdir(path)

    if len(files) == 0:
        print("Removing the empty folder:", path)
        os.rmdir(path)


def delete_oldest_file(dir):
    """
    Deletes the very oldest single file
    """

    if not os.path.isdir(dir):
        return False

    dir_list = os.listdir(dir)
    dir_list.sort()

    # loop through dir
    for name in dir_list:
        path = os.path.join(dir, name)

        if os.path.isfile(path):
            try:
                os.remove(path)
                return
            except:
                # print("ERROR: unable to delete - ", path)
                return

        if os.path.isdir(path):
            # check if directory is empty
            # print('DIRECTORY SIZE: ', path, '=', get_directory_size(path))

            if not get_directory_size(path):
                # print('Trying delete an empty folder:', path)
                # os.rmdir(path)
                remove_empty_folders(path)
                continue

            return delete_oldest_file(path)
