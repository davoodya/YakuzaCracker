# Step 1: Import all Requires Libraries

import sys

from os import path
from tkinter import ttk, filedialog, scrolledtext, messagebox, Tk
from PIL import Image, ImageTk

# Step 2: Initialize the Main Window
root = Tk()
root.title("Yakuza Cracker")
root.geometry("800x700")

# Step 3: Function to Get the Current Path to Bundled Resources (e.g., Logo, Image, ...)
def resource_path(relative_path):
    try:
        # get the current path which python file(gui.py) run in there
        if hasattr(sys, "_MEIPASS"):
            basePath = sys._MEIPASS     # noqa

        # if a python file runs in the IDE or Terminal, then get the path of the python file using __file__
        else:
            basePath = path.dirname(path.abspath(__file__))

    except Exception:   # noqa
        basePath = path.abspath(".")

    return path.join(basePath, relative_path)



