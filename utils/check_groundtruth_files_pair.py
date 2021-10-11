import os


def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    png_filename_wo_ext = []
    txt_filename_wo_ext = []

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            if filename.endswith(".png") or filename.endswith(".tif") or filename.endswith(".jpg"):
                png_filename_wo_ext.append(filename.split('.')[0])
            elif filename.endswith(".txt"):
                txt_filename_wo_ext.append(filename.split('.')[0])
    flag = False
    # check if there is a txt filename for each png filename
    for filename in png_filename_wo_ext:
        if filename not in txt_filename_wo_ext:
            flag = True
            print('File corresponding txt not found: ', filename)

    if flag is False:
        print('All files combination found in the directory.')


# Run the function to find the files that do not have a corresponding txt files
full_file_paths = get_filepaths("../data")
