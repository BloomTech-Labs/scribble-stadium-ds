"""
cpu_data_loader.py - Loads all data in the ../../data/transcribed_stories directory
"""
import glob
import os
import pathlib
import os.path as path

import keras_preprocessing.image.utils
import numpy as np
import tensorflow as tf
from tensorflow import keras


class PrePipelineStoryRef:
    def __init__(self, ground_truth_file: str, photos: list[str], id: str):
        self.ground_truth_file = ground_truth_file
        self.photos = photos
        self.base_directory = path.abspath(path.dirname(ground_truth_file))
        self.id = id

    def __repr__(self):
        return "Unprocessed Story File Reference: id:" + self.id + " base directory: " + self.base_directory


class PrePipelineDatasetRef:
    def __init__(self, story_refs: set, base_dir: str):
        self.story_refs = story_refs
        self.base_directory = base_dir

    def __repr__(self):
        return "Pre Pipeline Dataset reference object, containing: " + str(len(self.story_refs)) + " stories."

    def get_tf_dataset(self) -> tf.data.Dataset:
        photos_tensor = tf.keras.preprocessing.image_dataset_from_directory(self.base_directory, label_mode=None,
                                                                            color_mode="rgb", image_size=(1600, 1200))
        labels_tensor = ""

        return (photos_tensor, labels_tensor)


class CPUDataLoader:

    def __init__(self):
        self.data_path = path.abspath(path.join(path.dirname(__file__), "..", "..", "data", "transcribed_stories"))

    def get_file_structure(self) -> (list[PrePipelineStoryRef], str):
        # get the basic directory list
        directory_list = glob.glob(path.join(self.data_path, "*", "*"))

        # check to see that there are no errors in the list...
        identifier_list = [s.split(os.path.sep)[-1] for s in directory_list]
        identifier_set = set(identifier_list)

        if len(identifier_set) != len(identifier_list):
            print("dataset error, directory structure invalid")

        # check that all paths exist
        check_story_paths = set()
        for story_id in identifier_set:
            check_path = path.join(self.data_path, story_id[0:2] + "--", story_id)
            if path.exists(check_path):
                # print(check_path)
                check_story_paths.add(check_path)
            else:
                print("error path does not exist")

        # check that all stories have ground truth and at least one photo

        valid_story_paths = set()
        for check_path in check_story_paths:
            check_search_spec_photo = os.path.join(check_path, "*photo*")
            check_search_spec_story = os.path.join(check_path, "Story *")
            photos_in_path = glob.glob(check_search_spec_photo)
            storeys_in_path = glob.glob(check_search_spec_story)

            if len(storeys_in_path) == 1:
                if len(photos_in_path) >= 1:
                    story_id = check_path.split(os.path.sep)[-1]
                    valid_story_paths.add(
                        PrePipelineStoryRef(ground_truth_file=storeys_in_path[0], photos=photos_in_path, id=story_id))
                else:
                    print("error: invalid structure, story found but no photo: ", check_path)
            else:
                print("error: invalid structure, no story found: ", check_path)

        return valid_story_paths, self.data_path


if __name__ == "__main__":
    CDL = CPUDataLoader()
    file_structure = CDL.get_file_structure()
    print(file_structure)
    ref_dataset = PrePipelineDatasetRef(*file_structure)
    print(ref_dataset)
    for a in ref_dataset.story_refs:
        print(a)
    #tf_dataset = ref_dataset.get_tf_dataset()
    #print(tf_dataset)
    #for id in tf_dataset:
    #    print(id)
