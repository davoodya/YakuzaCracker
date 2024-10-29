# Step 1: Import all Requires Libraries

import sys

from os import path
from tkinter import ttk, filedialog, scrolledtext, messagebox, Tk
from PIL import Image, ImageTk

# Step 2: Initialize the Main Window
root = Tk()
root.title("Yakuza Cracker")
root.geometry("800x700")

# Step 3: Function to Get the Current Path to Bundled Resources (e.g., Logo, Image, ...) for PyInstaller
def resource_path(relative_path):
    try:
        # if gui.py bundled with PyInstaller,
        # to get the current path of where gui.py run in there, we should use sys._MEIPASS
        if hasattr(sys, "_MEIPASS"):
            basePath = sys._MEIPASS     # noqa

        # if a python file runs in the IDE or Console, then to get the current path of where gui.py run in there,
        # We should use __file__ in the dirname(abspath(__file__))
        else:
            basePath = path.dirname(path.abspath(__file__))

    except Exception:   # noqa
        basePath = path.abspath(".")

    return path.join(basePath, relative_path)



