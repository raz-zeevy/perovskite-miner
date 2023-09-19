"""
Paper Scraper
This script scrapes papers from sci-hub using selenium and chrome webdriver
The script takes a list of dois and downloads the pdfs to the output folder
Args:
    # TODO: add this feature
    dois (.txt, .csv): a text file containing the dois to scrape
                        delimted by newlines or commas.
    output (str): output folder
    # TODO: add option to insert the chromedriver path
    chromedriver (str): path to chromedriver
    --debug (bool): debug mode
    # TODO: add option to check that download is not currapted
        right now there are some papers that are downloaded but are currapted
"""
import argparse
import os
import numpy as np
import requests
import re
import winsound
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import selenium
import time

SCRAPER_CACHE_FILENAME = 'scraper_cache'

DEBUG_MODE = False

def urlencode(s):
    # urlencode <string>
    # Use Python's urllib.parse.quote to encode the string
    from urllib.parse import quote
    return quote(s, safe='')

def beep_on_error(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            winsound.Beep(500,1000)  # Frequency: 500Hz, Duration: 1000ms (1 second)
            if DEBUG_MODE:
                print(e)
                time.sleep(3000)
    return wrapper

def get_driver():
    chrome_options = Options()
    if not DEBUG_MODE:
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
def scrape_list(doi_list, no_cache=False):
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
            if not no_cache:
                with open(SCRAPER_CACHE_FILENAME,'a') as f:
                    f.write(f"{doi}\n")
            continue
        source = pdf_iframe.get_attribute("src")
        # download the pdf from the src
        # write_pdf(driver, source, f"{urlencode(doi)}.pdf")
        if write_pdf(source, os.path.join(output_folder, f"{sanitize(doi)}.pdf")):
            print("****************")
            print(f"Downloaded {doi}")
            print("****************")

def load_dois_from_cache(cache_path):
    dois = []
    with open(cache_path, "r") as f:
        for line in f:
            dois.append(line.strip())
    return dois

def dois_to_download(doi_list, output_folder):
    lst = [doi for doi in doi_list if not os.path.exists(
        os.path.join(output_folder, f"{sanitize(doi)}.pdf"))]
    dois_not_found =  load_dois_from_cache(SCRAPER_CACHE_FILENAME)
    lst = [doi for doi in lst if doi not in dois_not_found]
    return lst

if __name__ == '__main__':
    # add argument --debug from the execution paramters to enable debug mode
    # using argparse
    parser = argparse.ArgumentParser(
        description='Download papers from sci-hub')
    parser.add_argument('--debug', action='store_true',
                        help='enable debug mode')
    parser.add_argument('--no-cache', action='store_true',
                        help="don't write a list of papers that are not in "
                             "sci-hub to a file")
    args = parser.parse_args()
    if args.debug:
        DEBUG_MODE = True
    if not args.no_cache:
        if not os.path.exists(SCRAPER_CACHE_FILENAME):
            with open(SCRAPER_CACHE_FILENAME, "w") as f:
                pass
    output_folder = 'data/papers/downloads'
    doi_list = np.loadtxt('data/papers/doi-list.txt', delimiter=",", dtype=str)
    # remove doi's that have already been downloaded or not found
    doi_list = dois_to_download(doi_list, output_folder)
    while doi_list:
        scrape_list(doi_list, no_cache = args.no_cache)
        doi_list = dois_to_download(doi_list, output_folder)
