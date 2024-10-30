""" YakuzaCracker - an Advanced GUI Tool for Cracking ZIP, RAR and MS-Office Documents,
    Also yakuzaCracker can Perform Reverse Bruteforce Attacks to Crack the Login Pages on the http and https.

Author: Davood Yakuza from Iran, Isfahan
Last Update: 29/10/2024 --- 8 aban 1403"""

""" Section 1: Import all Requires Libraries and Basic Configurations """

# Step 0: Import all Requires Libraries 
import sys
import logging

from colorama import init
from os import path
from msoffcrypto import OfficeFile
from io import BytesIO
from pyzipper import AESZipFile


# Step 1: Initialize colorama for colored console output
init()

# Step 2: Setup logging configuration
logging.basicConfig(filename="yakuza_cracker.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Step 3: Define global variables
stopFlag = False    # stopFlag used to stop the cracking process

results = []    # result's list use to store the cracked(founded) passwords


""" Section 2: Developing Utility Functions """

# Step 4: Function to Get the Path to Bundled Resources in PyInstaller
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


""" Step 5: Function to Try a Password on Different File Types """
def try_password(file_path, file_type, password):
    logging.info(f"[+] Trying password: {password}")
    
    try:
        # If the file is an Office file, then execute try_office_password
        if file_type in ['xls', 'xlsx', 'doc', 'docx']:
            return try_office_password(file_path, password)

        # If the file is ZIP File, then execute try_zip_password()
        elif file_type == 'zip':
            return try_zip_password(file_path, password)

        # If the file is PDF File, then execute try_pdf_password()
        elif file_type == 'pdf':
            return try_pdf_password(file_path, password)

        else:
            logging.error("[-] Unsupported file type.")
            return False

    except Exception as e:
        logging.error(f"[-] Error Trying password: {password} | Error: {e}")
        return False

# Step 6: Define a function to try passwords on MS Office files
def try_office_password(file_path, password):
    # Read Office file
    with open(file_path, 'rb') as f:
        file = OfficeFile(f)
        file.load_key(password=password)

        with BytesIO() as decrypted:
            file.decrypt(decrypted)
            return True

# Step 7: Define a function to try passwords on ZIP files
def try_zip_password(file_path, password):
    # Open the ZIP file and attempt to extract it using pyzipper
    with AESZipFile(file_path) as zf:
        zf.extractall(pwd=password.encode('utf-8'))
        return True


def try_pdf_password(file_path, password):
    pass





























