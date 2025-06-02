**PLC Watch Table Reader** is a Python desktop application designed to communicate with local PLC (Programmable Logic Controller) web servers. It allows users to retrieve "watch tables" (variable tables), filter relevant data, and export it to CSV files using a simple graphical interface.

---

## ⚙️ Purpose

This tool is intended for maintenance technicians, automation engineers, or any professional who needs to:

- Access and monitor PLC data via internal web servers
- Automatically extract watch/observation tables
- Store logs of variable values, comments, and states in `.csv` format for further analysis or documentation

It was designed with usability and efficiency in mind, especially for environments where PLCs expose their data over HTTP through embedded web interfaces.

---

## 📦 Features

- GUI to manage multiple PLC IPs and corresponding line names
- Automatically fetch available watch tables per PLC
- Extract relevant fields: variable name, value and comment
- Save data to timestamped `.csv` files
- Add/remove PLCs dynamically
- Automatic error logging to `/logs/`

---

## 🛠️ Technical Requirements

To run and develop **PLC Watch Table Reader**, the following software and libraries are required:

### Software

- **Python 3.7 or higher**  
  The project is built and tested with Python 3.7+.

- **Internet access** (optional)  
  Required for downloading watch tables from PLC web interfaces via HTTP.

### Python Libraries

```{r, engine='bash', eval=FALSE}
# Install dependencies with pip:
pip install pandas requests beautifulsoup4 pillow
```

## 📚 Basic Knowledge Required

To effectively use and modify the application code, familiarity with the following is recommended:

- **Python programming**  
  Understanding of core Python syntax, functions, classes, and exception handling (`try-except`).

- **Tkinter GUI framework**  
  Basics of creating windows, widgets (buttons, labels, frames), event handling, and layout management.

- **HTTP Requests and Web Scraping**  
  Use of `requests` to perform HTTP GET requests and `BeautifulSoup` for HTML parsing and data extraction.

- **Data manipulation with Pandas**  
  Reading HTML tables into DataFrames, filtering columns, and exporting CSV files.

- **File and directory operations**  
  Reading/writing text files, managing directories, and working with relative and absolute paths.

- **Logging and error management**  
  Configuring and using the `logging` module to capture runtime errors and debugging information.

- **Basic networking concepts**  
  Understanding IP addresses and network accessibility of PLC devices for data retrieval.
