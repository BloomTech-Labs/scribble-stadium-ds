"""
cpu_data_loader.py - Loads all data in the ../../data/transcribed_stories directory
"""
import pathlib
import os.path as path


class CPUDataLoader():
    def __init__(self):
        self.data_path = path.join(path.dirname(__file__), "..", "..", "data", "transcribed_stories")
