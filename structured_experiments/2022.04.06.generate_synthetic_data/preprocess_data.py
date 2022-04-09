"""
This module takes in a list of directories containing text (.txt) files. It provides the functionality to place
a string filepath to each file and place each within the same list. It then provides a function to split the text
on punctuation to extract individual sentences. These sentences are returned as a list.
"""

from pathlib import Path
import re


def get_data_files(data_files):
    """
    Extracts the files from each directory in the supplied list and returns a list of those files as string objects.
    ==========

    input   : Text file
    output  : String containing the contents of the file supplied to the module.
    """

    file_list = []

    for directory in data_files:
        directory = Path(directory)
        for file in directory.iterdir():
            if Path.is_file(file) and file.name[-4:] == '.txt':
                file_path = directory.name + '/' + file.name
                file_list.append(file_path)
            else:
                continue

    return file_list


def split_data(data_paths):
    """
    Splits text document on '.', '?', and '!' to extract sentences. This will allow the data
    to provide context to the Tesseract model for each word and character.
    ==========

    input   : text file with punctuation
    output  : list of sentences from the input
    """

    split_file_list = []

    for file in data_paths:
        file = Path(file)

        text = file.read_text('UTF-8')
        split_text = re.split('(?<=[.!?]) +', text)

        split_file_list.append(split_text)

    return split_text
