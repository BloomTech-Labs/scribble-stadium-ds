"""
cpu_data_loader.py - Loads all data in the ../../data/transcribed_stories directory
"""
import pathlib
import os


class CPUDataLoader():
    def __init__(self):
        self.data_path = os.path.join("..", "..", "data", "transcribed_stories")
