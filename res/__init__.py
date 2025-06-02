import os
import sys
from datetime import datetime
import logging

# Base path
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    INPUT_DIR = os.path.join(BASE_DIR, '.', 'input')
    OUTPUT_DIR = os.path.join(BASE_DIR, '.', 'output')
    ASSETS_DIR = os.path.join(BASE_DIR, '.', 'assets')
    LOGS_DIR = os.path.join(BASE_DIR, '.', 'logs')
    TXT_IPS = os.path.join(INPUT_DIR, 'ips.txt')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIR = os.path.join(BASE_DIR, '..', 'input')
    OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'output')
    ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets')
    LOGS_DIR = os.path.join(BASE_DIR, '..', 'logs')
    TXT_IPS = os.path.join(INPUT_DIR, 'ips.txt')

# Ensure folders exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Logging
log_file = os.path.join(LOGS_DIR, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)