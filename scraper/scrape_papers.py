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
    --no-cache (bool): disable caching
    --safe-mode (bool): safe mode
    --verbose (bool): print, print+sound, none
"""
import argparse
import os
from datetime import datetime

import numpy as np
import requests
import re
import winsound
from numpy import ndarray
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import selenium
import time
from pypdf import PdfReader, errors

DEFAULT_DOWNLOADS_FOLDER = "downloads"

# <------------    API Constants
VERBOSE_OPTIONS = ['none', 'info', 'verbose', 'verbose+sound']

# <------------    Massages Constants
m_MARGIN_FAILURE = "###########"
m_MARGIN_SUCCESS = "***********"
m_DOWNLOAD_FAILED = "Error downloading {source} status: {status_code}, " \
                    "reason: {reason}"
m_DOWNLOAD_SUCCESS = "Downloaded %s"
m_DOWNLOAD_CORRUPTED = "invalid file download: %s\n removing file and retrying"

# <------------    Scraper Constants
SCRAPER_CACHE_FILENAME = 'scraper_cache'
SCI_HUB_URL = 'https://sci-hub.hkvisa.net'
DEBUG_ATTEMPTS = 20
ATTEMPTS = 10

def urlencode(s):
    # urlencode <string>
    # Use Python's urllib.parse.quote to encode the string
    from urllib.parse import quote
    return quote(s, safe='')


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

class PaperScraper:
    def __init__(self, DOI_list_path: str,
                 output_folder: str = None,
                 debug: bool = False,
                 no_cache: bool = False,
                 safe_mode: bool = False,
                 verbose: str = 'none'):
        self.output_folder = self.init_output_folder(output_folder)
        self.DOI_list = self.load_doi_list(DOI_list_path)
        self.debug = debug
        self.no_cache = no_cache
        self.safe_mode = safe_mode
        self.verbose = verbose if not debug else VERBOSE_OPTIONS[-1]
        #
        self.attempts = DEBUG_ATTEMPTS if safe_mode else ATTEMPTS
        self.cache_path = self.init_cache()
        self.doi_attempts = {}
        self.current_doi = None

    def get_driver(self):
        chrome_options = Options()
        if not self.debug:
            chrome_options.add_argument('--headless')  # Run headless
            chrome_options.add_argument(
                '--disable-gpu')  # Disable GPU acceleration (needed for some headless setups)
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options)

    def load_doi_list(self, doi_list: str) -> ndarray:
        try:
            return np.loadtxt(doi_list, delimiter=",",
                              dtype=str)
        except FileNotFoundError:
            print(f"Could not find file: {doi_list}")
            exit(1)

    def init_output_folder(self, output_folder: str) -> str:
        if not output_folder:
            output_folder = DEFAULT_DOWNLOADS_FOLDER
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        return output_folder

    def init_cache(self) -> str:
        cache_path = SCRAPER_CACHE_FILENAME
        if not os.path.exists(cache_path):
            if not self.no_cache:
                with open(cache_path, "w") as f:
                    pass
        return cache_path

    def loop_scrape(self):
        cur_doi_list = self.dois_to_download()
        while cur_doi_list:
            try:
                self.scrape_list(cur_doi_list, no_cache=args.no_cache)
            except Exception as e:
                self.log(f"Unexpected error occurred during: {self.current_doi}",
                        level="info")
                self.log(f"Error: {e}", level='verbose')
                if self.verbose == VERBOSE_OPTIONS[-1]:
                    # Frequency: 500Hz, Duration: 1000ms (1 second)
                    winsound.Beep(500, 1000)
                if self.debug:
                    raise e
            finally:
                cur_doi_list = self.dois_to_download()

    def scrape_list(self, doi_list, no_cache=False):
        driver = self.get_driver()
        for doi in doi_list:
            # for logging
            if doi not in self.doi_attempts: self.doi_attempts[doi] = 1
            self.current_doi = doi
            #
            url = f'{SCI_HUB_URL}/{urlencode(doi)}'
            driver.get(url)
            # find the pdf by the id="pdf"
            try:
                pdf_iframe = driver.find_element("id", "pdf")
            except selenium.common.exceptions.NoSuchElementException:
                wait = WebDriverWait(driver, 3)  # Adjust the timeout as needed
                element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     "//p[@id='request' and text()='Sorry, sci-hub has not included this article yet']")))
                if not no_cache:
                    with open(self.cache_path, 'a') as f:
                        f.write(f"{doi}\n")
                continue
            source = pdf_iframe.get_attribute("src")
            pdf_path = os.path.join(self.output_folder,
                                    f"{sanitize(doi)}.pdf")
            if self.save_pdf_to_disk(source, pdf_path):
                self.log((m_DOWNLOAD_SUCCESS % doi), success=True,
                         level="info")
                if self.safe_mode:
                    self.validate_download(pdf_path)
            self.doi_attempts[doi] += 1

    def load_dois_from_cache(self):
        dois = []
        with open(self.cache_path, "r") as f:
            for line in f:
                dois.append(line.strip())
        return dois

    def dois_to_download(self):
        lst = [doi for doi in self.DOI_list if not os.path.exists(
            os.path.join(self.output_folder, f"{sanitize(doi)}.pdf"))]
        dois_not_found = self.load_dois_from_cache()
        lst = [doi for doi in lst if doi not in dois_not_found]
        return lst

    def validate_download(self, file_path):
        try:
            text = PdfReader(file_path)
        except errors.EmptyFileError:
            self.log(m_DOWNLOAD_CORRUPTED % self.current_doi, level="verbose")
        os.remove(file_path)

    def save_pdf_to_disk(self, source, dest):
        for _ in range(self.attempts):
            res = requests.get(source)
            if res.status_code != 200:
                self.log(m_DOWNLOAD_FAILED.format(source=source,
                                                  status_code=res.status_code,
                                                  reason=res.reason),
                         level="verbose")
                self.doi_attempts[self.current_doi] += 1
                continue
            with open(dest, "wb") as f:
                f.write(res.content)
                return True
        self.log("Couldn't scrape %s in this epoch" % self.current_doi,
                 level="info")
        return False

    def check_verbose_level(self, level):
        if level in VERBOSE_OPTIONS:
            return VERBOSE_OPTIONS.index(level) <= VERBOSE_OPTIONS.index(
                self.verbose)

    def log(self, log_msg, success=False, level=None):
        if not self.check_verbose_level(level): return
        if self.verbose == VERBOSE_OPTIONS[0]: return
        timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        margin = m_MARGIN_SUCCESS if success else ""
        if success: print(margin)
        print(f"{timestamp} - {log_msg} ("
              f"{self.doi_attempts.get(self.current_doi, '')})")
        if success: print(margin)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='PaperScraper',
        description='Download papers from sci-hub')
    parser.add_argument('doi_list_path', type=str,
                        help='path to the doi list file, should be a txt '
                             'file that is delimited by new line', )
    parser.add_argument('--output-folder', type=str,
                        help='path to the output folder', )
    # todo: more exlpatnion about the deubg mode
    parser.add_argument('--debug', action='store_true',
                        help='enable debug mode', )
    parser.add_argument('--no-cache', action='store_true',
                        help="don't write a list of papers that are not in "
                             "sci-hub to a file", )
    parser.add_argument('--safe-mode', action='store_true',
                        help="Increase maximum tries for each paper and check "
                             "for each paper if it has been downloaded"
                             "correctly and if not, try to download it again", )
    # todo: add retain head option
    parser.add_argument('--verbose', choices=VERBOSE_OPTIONS,
                        default='none', help='verbosity level')
    return parser.parse_args()


def run_example_1():
    args.doi_list_path = '../dataset/papers/doi-list.txt'
    # args.output_folder = 'downloads'
    # args.debug = True
    # args.no_cache = False
    args.safe_mode = True
    args.verbose = 'info'


def run_example_2():
    args.doi_list_path = '../dataset/papers/doi-list.txt'
    args.output_folder = '../data/papers/downloads'
    args.debug = False
    args.no_cache = False
    args.safe_mode = False
    args.verbose = 'info'


if __name__ == '__main__':
    args = parse_args()
    run_example_2()
    PaperScraper(args.doi_list_path, args.output_folder,
                 debug=args.debug, no_cache=args.no_cache,
                 safe_mode=args.safe_mode, verbose=args.verbose).loop_scrape()
