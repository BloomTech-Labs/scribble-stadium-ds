"""
This module takes in a list of directories containing text (.txt) files. It provides the functionality to place
a string filepath to each file and place each within the same list. It then provides a function to split the text
on punctuation to extract individual sentences. These sentences are returned as a list.
"""

from pathlib import Path
from sys import argv


if len(argv) < 2:
    raise Exception('Supply at least one path to a directory containing a valid text file(s).')
for i in argv[1:]:
    if not Path(i).is_dir():
        raise NotADirectoryError(f'{argv[argv.index(i)]} at index {argv.index(i)} is not a valid directory')


def get_data_files(data_file):
    """
    Extracts the files from each directory in the supplied list and returns a list of those files as string objects.
    ==========

    input   : Text file
    output  : String containing the contents of the file supplied to the module.
    """

    dir_list = argv[1:]
    file_list = []

    for directory in dir_list:
        directory = Path(directory)
        for file in directory.iterdir():
            if Path.is_file(file) and file.name[-4:] == '.txt':
                file_list.append(file.name)
            else:
                continue

    return file_list


def split_data(data_path):
    """
    Splits text document on '.', '?', and '!' to extract sentences. This will allow the data
    to provide context to the Tesseract model for each word and character.
    ==========

    input   : text file with punctuation
    output  : list of sentences from the input
    """



    pass


get_file('some_file.txt')
