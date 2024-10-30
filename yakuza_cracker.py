""" YakuzaCracker - an Advanced GUI Tool for Cracking ZIP, RAR and MS-Office Documents,
    Also yakuzaCracker can Perform Reverse Bruteforce Attacks to Crack the Login Pages on the http and https.

Author: Davood Yakuza from Iran, Isfahan
Last Update: 29/10/2024 --- 8 aban 1403"""

""" Section 1: Import all Requires Libraries and Basic Configurations """

""" Step 0: Import all Requires Libraries """
import sys
import logging

from colorama import init
from os import path

""" Step 1: Initialize colorama for colored console output """
init()

""" Step 2: Setup logging configuration """
logging.basicConfig(filename="yakuza_cracker.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


""" Step 3: Define global variables """

# stopFlag used to stop the cracking process
stopFlag = False

# result's list use to store the cracked(founded) passwords
results = []



""" Section 2: Developing Utility Functions """

""" Step 4: Function to Get the Path to Bundled Resources in PyInstaller """
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





























