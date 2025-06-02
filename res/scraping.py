import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from . import OUTPUT_DIR

def fetch_table_names(ip):
    url = f"http://{ip}/Portal/Portal.mwsl?PriNav=Vartables"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        select = soup.find('select', {'name': 'ThrNav'})
        if not select:
            raise ValueError("Select element not found")

        return {opt.text.strip(): idx + 1 for idx, opt in enumerate(select.find_all('option'))}
    except Exception as e:
        logging.exception(f"Error fetching table list from {ip}")
        raise e

def download_table(ip, table_name, index, line_name):
    url = f"http://{ip}/Portal/Portal.mwsl?PriNav=Vartables&ThrNav=Vartable_{index}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        html_table = soup.find('table', class_='Vartable s7webtable')

        if not html_table:
            return None

        df = pd.read_html(str(html_table))[0]
        df_filtered = df.iloc[:, [0, 3, 4]]
        df_filtered.columns = ['Name', 'Value', 'Comment']

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{line_name}_{table_name}_{timestamp}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        df_filtered.to_csv(filepath, index=False, header=None)
        return filename
    except Exception as e:
        logging.exception(f"Error processing table '{table_name}' from {ip}")
        raise e