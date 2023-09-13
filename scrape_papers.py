import os
import subprocess

import numpy as np
import requests
import re

import winsound
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import selenium
import time
import pandas as pd

def urlencode(s):
    # urlencode <string>
    # Use Python's urllib.parse.quote to encode the string
    from urllib.parse import quote
    return quote(s, safe='')

def beep_on_error(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            winsound.Beep(500,1000)  # Frequency: 500Hz, Duration: 1000ms (1 second)
    return wrapper

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless
    chrome_options.add_argument(
        '--disable-gpu')  # Disable GPU acceleration (needed for some headless setups)
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options)

def write_pdf(source,dest):
    res = requests.get(source)
    if res.status_code != 200:
        print(f"Error downloading {source}")
        print(f"status: {res.status_code}, reason: {res.reason}")
        print("###########")
        return False
    with open(dest, "wb") as f:
        f.write(res.content)
        return True
def sanitize(filename):
    # Define a regex pattern to match characters not allowed in file names
    invalid_chars = r'[\/:*?"<>|]'
    # Replace invalid characters with underscores
    sanitized_filename = re.sub(invalid_chars, '_', filename)
    # Trim any leading or trailing spaces and dots
    sanitized_filename = sanitized_filename.strip('. ')
    # Ensure the filename is not empty
    if not sanitized_filename:
        sanitized_filename = 'unnamed_file'
    return sanitized_filename

@beep_on_error
def scrape_list(doi_list):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    driver = get_driver()
    for doi in doi_list:
        url = f'https://sci-hub.hkvisa.net/{urlencode(doi)}'
        driver.get(url)
        # find the pdf by the id="pdf"
        try:
            pdf_iframe = driver.find_element("id", "pdf")
        except selenium.common.exceptions.NoSuchElementException:
            wait = WebDriverWait(driver, 3)  # Adjust the timeout as needed
            element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                 "//p[@id='request' and text()='Sorry, sci-hub has not included this article yet']")))
            continue
        source = pdf_iframe.get_attribute("src")
        # download the pdf from the src
        # write_pdf(driver, source, f"{urlencode(doi)}.pdf")
        if write_pdf(source, os.path.join(output_folder, f"{sanitize(doi)}.pdf")):
            print(f"Downloaded {doi}")

if __name__ == '__main__':
    output_folder = 'data/papers/downloads'
    doi_list = np.loadtxt('data/papers/doi-list.txt', delimiter=",", dtype=str)
    # remove doi's that have already been downloaded
    doi_list = [doi for doi in doi_list if not os.path.exists(
        os.path.join(output_folder, f"{sanitize(doi)}.pdf"))]
    while doi_list:
        scrape_list(doi_list)
        doi_list = [doi for doi in doi_list if not os.path.exists(
            os.path.join(output_folder, f"{sanitize(doi)}.pdf"))]

