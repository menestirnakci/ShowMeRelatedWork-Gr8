import requests
import os
import shutil
from pathlib import Path
import time
from ctypes import wintypes, WINFUNCTYPE
import signal
import ctypes
import mmap
import sys

# Function prototype for the handler function. Returns BOOL, takes a DWORD.
HandlerRoutine = WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)

def _ctrl_handler(sig):
    """Handle a sig event and return 0 to terminate the process"""
    if sig == signal.CTRL_C_EVENT:
        dir_path = Path('./static/pdf')
        shutil.rmtree(dir_path)
    elif sig == signal.CTRL_BREAK_EVENT:
        dir_path = Path('./static/pdf')
        shutil.rmtree(dir_path)
    else:
        print("UNKNOWN EVENT")
    return 0

ctrl_handler = HandlerRoutine(_ctrl_handler)


SetConsoleCtrlHandler = ctypes.windll.kernel32.SetConsoleCtrlHandler
SetConsoleCtrlHandler.argtypes = (HandlerRoutine, wintypes.BOOL)
SetConsoleCtrlHandler.restype = wintypes.BOOL

if __name__ == "__main__":
    # Add our console control handling function with value 1
    if not SetConsoleCtrlHandler(ctrl_handler, 1):
        print("Unable to add SetConsoleCtrlHandler")
        exit(-1)

    if not os.path.exists('./static/pdf'):
        os.makedirs('./static/pdf')
        
    url = 'https://www.researchgate.net/profile/Mahmoud_Al-Dalahmeh/publication/326319011_Intellectual_capital_knowledge_management_and_social_capital_within_the_ICT_sector_in_Jordan/links/5b45d1d6458515b4f662d3b6/Intellectual-capital-knowledge-management-and-social-capital-within-the-ICT-sector-in-Jordan.pdf'

    r = requests.get(url)

    with open('./static/pdf/metadata.pdf', 'wb') as f:
        f.write(r.content)

    # Do nothing but wait for the signal
    while True:
        pass
    
#dir_path = Path('./static/pdf')
#shutil.rmtree(dir_path)

