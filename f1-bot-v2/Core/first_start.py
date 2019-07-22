# -*- coding: utf-8 -*-
import os

class Start:
    """
    Checks whether it is the first time the program started by seeing if a file exists or not
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def is_first(self):
        return not os.path.isfile(self.file_path)
