""" YakuzaCracker - an Advanced GUI Tool for Cracking ZIP, RAR and MS-Office Documents,
    Also yakuzaCracker can Perform Reverse Bruteforce Attacks to Crack the Login Pages on the http and https.

Author: Davood Yakuza from Iran, Isfahan
Last Update: 29/10/2024 --- 8 aban 1403"""

""" Step 1: Import all Requires Libraries """

import sys

from os import path
from tkinter import ttk, filedialog, scrolledtext, messagebox, Tk, StringVar, Label
from PIL import Image, ImageTk

""" Step 2: Initialize the Main Window """
root = Tk()
root.title("Yakuza Cracker")
root.geometry("800x700")

""" Step 3: Function to Get the Current Path to Bundled Resources (e.g., Logo, Image, ...) for PyInstaller """
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

""" Step 4: Set the Icon for the Window """

# open logo.png using resource_path()
logo = Image.open(resource_path("img/logo.png"))

# resize logo.png
logo = logo.resize((64, 64), Image.LANCZOS) # noqa

# Prepare Logo image to use in the tkinter UI
logo = ImageTk.PhotoImage(logo)

# Set Logo in the main gui
root.iconphoto(False, logo) # noqa

""" Step 5: Create the Main Frame """
mainFrame = ttk.Frame(root, padding="10")
mainFrame.grid(row=0, column=0, sticky="nsew")


""" Step 6: Configure styles for the UI components """
# Create style Instance
style = ttk.Style()

# Configure new style for Labels in named TLabel
style.configure("TLabel", background="#05050F", foreground="#FFD700")

# Configure new style for Frames in named TFrame
style.configure("TFrame", background="#05050F")

# Configure new style for Buttons in named TButton
style.configure("TButton", background="black", foreground="red", bordercolor="#009933",
                focusthickness=3, focuscolor="None")

# Configure new style for Horizontal Progressbar in named Green.Horizontal.TProgressbar
style.configure("Green.Horizontal.TProgressbar",troughcolor="#151525", background="#00FF00", bordercolor="05050F")


""" Step 7: Add the attack type selection components """

# Create String Variable to store brute_force
attackTypeVar = StringVar(value="brute_force")

# Create Label in main_frame with text => Select Attack Type:
attackTypeLabel = Label(mainFrame, text="Select Attack Type:", font=("Courier New", 12))

# Set Position of Label in the Main Frame
attackTypeLabel.grid(row=0, column=0, pady=5, padx=5, sticky="w")

# Create new Combobox to show attack_type_var(brute_force) as first item
attackTypeMenu = ttk.Combobox(mainFrame, textvariable=attackTypeVar, state="readonly", font=("Consolas", 12))

# Create Values of the Combobox
attackTypeMenu["values"] = ("brute_force", "dictionary", "reverse_brute_force")

# Set position of Combobox in the Main Frame
attackTypeMenu.grid(row=0, column=1, pady=5, padx=(0, 5), sticky="w")


""" Step 8: Add the file type selection frame """
# Create ttk.Frame with TFrame style
fileTypeFrame = ttk.Frame(mainFrame, style="TFrame")

# Create Label for file type selection
fileTypeLabel = Label(fileTypeFrame, text="Select File Type:", font=("Courier New", 12))

# Set Label Position on the UI
fileTypeLabel.grid(row=0, column=0, pady=5, padx=5, sticky="w")

# Create StringVar to store the first item of Combo Box => 'zip'
fileTypeVar = StringVar(value="zip")

# Create Combo Box in the fileTypeFrame with fileTypeVar(zip)
fileTypeMenu = ttk.Combobox(fileTypeFrame, textvariable=fileTypeVar, state="readonly", font=("Consolas", 12))

# Create other Value's of Combo Box
fileTypeMenu["values"] = ("zip", "xls", "doc", "pdf")

# Set Position of fileTypeMenu and fileTypeFrame
fileTypeMenu.grid(row=0, column=1, pady=5, padx=(0, 5), sticky="w")
fileTypeFrame.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky="ew")


""" Step 9: Add the brute force configuration frame """

# Step 9.1: Create brute force frame
bruteForceFrame = ttk.Frame(mainFrame, style="TFrame")

# Step 9.2: Create Label for brute force frame
ttk.Label(bruteForceFrame, text="FilePath:", font=("Courier New", 12)).grid(row=2, column=0, pady=5, padx=5, sticky="w")

# Step 9.3: Create File Path Entry
filePathEntry = ttk.Entry(bruteForceFrame, width=40, font=("Consolas", 12), background="#151525", foreground="red")
filePathEntry.grid(row=2, column=1, pady=5, padx=5, sticky="w")

# Step 9.4: Create a Browse Button
ttk.Button(bruteForceFrame, text="Browse", style="TButton").grid(row=2, column=2, pady=5, padx=5, sticky="w")

# Step 9.5: Create MAX Length Label
ttk.Label(bruteForceFrame, text="Max Length:", font=("Courier New", 12)).grid(row=3, column=0, pady=5, padx=5, sticky="w")

# Step 9.6: Create MAX Length Entry
maxLengthEntry = ttk.Entry(bruteForceFrame, width=10, font=("Consolas", 12), background="#151525", foreground="red")
maxLengthEntry.grid(row=3, column=1, pady=5, padx=5, sticky="w")

# Step 9.7: Create Charset Label
ttk.Label(bruteForceFrame, text="Charset:", font=("Courier New", 12)).grid(row=4, column=0, pady=5, padx=5, sticky="w")

# Step 9.8: Create Charset Entry
charsetEntry = ttk.Entry(bruteForceFrame, width=40, font=("Consolas", 12), background="#151525", foreground="red")
charsetEntry.grid(row=4, column=1, pady=5, padx=5, sticky="w")


""" Step 10: Add the Dictionary Attack Configuration Frame """

# Step 10.1: Create Filepath Label











# For testing
mainFrame.mainloop()