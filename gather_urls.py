from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import bs4
import pickle
from web_scraping_utils import *

def gather_urls(search_range, start_date, stop_date):
    """Initialize Web Driver"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(10)

    """Get Study URLs"""
    if search_range:
        results_URL = 'https://clinicaltrials.gov/ct2/results?cond=&term=&type=&rslt=&age_v=&gndr=&intr=&titles=&outc' + \
                      '=&spons=&lead=&id=&cntry=&state=&city=&dist=&locn=&rsub=&strd_s=&strd_e=&prcd_s=&prcd_e=&sfpd_' + \
                      's=&sfpd_e=&rfpd_s=&rfpd_e=&lupd_s=' + start_date[0] + '%2F' + start_date[1] + '%2F' + \
                      start_date[2] + '&lupd_e=' + stop_date[0] + '%2F' + stop_date[1] + '%2F' + stop_date[2] + '&sort='
    else:
        results_URL = "https://clinicaltrials.gov/ct2/results?recrs=ab&cond=&term=&cntry=&state=&city=&dist="

    # read results webpage
    driver.get(results_URL)
    time.sleep(1)  # wait for page to load
    results_page = bs4.BeautifulSoup(driver.page_source, "html.parser")

    # change number of studies per page from 10 to 100
    select = Select(driver.find_element_by_name('theDataTable_length'))  # get drop down menu
    select.select_by_value('100')  # select 100
    time.sleep(1)  # wait for page to load
    results_page = bs4.BeautifulSoup(driver.page_source, "html.parser")  # read results page again

    # find out how many pages of results to expect
    num_results = int(results_page.find(id='theDataTable_info').find('b').text.replace(',', ''))  # total num of results
    num_pages = int(num_results / 100)  # divide by num of results per page

    # get study hyperlinks from page
    study_urls = []
    study_urls = get_urls_from_page(results_page, study_urls)
    for i in range(num_pages):
        # click next button for new page of results
        next_button = driver.find_element_by_id("theDataTable_next")
        if next_button.is_displayed():
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(.2)

        # read results page again
        results_page = bs4.BeautifulSoup(driver.page_source, "html.parser")

        # get study hyperlinks from page
        study_urls = get_urls_from_page(results_page, study_urls)

    # save URLs to file
    with open('study_urls.pickle', 'wb') as handle:
        pickle.dump(study_urls, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("\tURLs successfully saved to study_urls.pickle")

    return study_urls