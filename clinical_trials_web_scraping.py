import requests
import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pickle
import csv
from web_scraping_utils import *

"""Initialization"""
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=options)
driver.implicitly_wait(10)

"""Get Study URLs"""
# results_URL = "https://clinicaltrials.gov/ct2/results?recrs=ab&cond=&term=&cntry=&state=&city=&dist="
#
# # read results webpage
# driver.get(results_URL)
# time.sleep(1) # wait for page to load
# results_page = bs4.BeautifulSoup(driver.page_source, "html.parser")
#
# # change number of studies per page from 10 to 100
# select = Select(driver.find_element_by_name('theDataTable_length')) # get drop down menu
# select.select_by_value('100') # select 100
# time.sleep(1) # wait for page to load
# results_page = bs4.BeautifulSoup(driver.page_source, "html.parser") # read results page again
#
# # find out how many pages of results to expect
# num_results = int(results_page.find(id='theDataTable_info').find('b').text.replace(',', '')) # total number of results
# num_pages = int(num_results / 100) # divide by number of results per page
#
# # get study hyperlinks from page
# study_urls = []
# study_urls = get_urls(results_page, study_urls)
# for i in range(num_pages):
#     # click next button for new page of results
#     next_button = driver.find_element_by_id("theDataTable_next")
#     if next_button.is_displayed():
#         driver.execute_script("arguments[0].click();", next_button)
#         time.sleep(.2)
#
#     # read results page again
#     results_page = bs4.BeautifulSoup(driver.page_source, "html.parser")
#
#     # get study hyperlinks from page
#     study_urls = get_urls(results_page, study_urls)
#
# # save URLs to file
# with open('study_urls.pickle', 'wb') as handle:
#     pickle.dump(study_urls, handle, protocol=pickle.HIGHEST_PROTOCOL)

"""Read Study URLs from file"""
# with open('20210325_study_urls.pickle', "rb") as handle:
#     study_urls = pickle.load(handle)

"""Gather Study Information"""
# home_url = 'https://clinicaltrials.gov'
# data = []
# for url in study_urls:
#     # open webpage
#     page = requests.get(home_url+url)
#     soup = bs4.BeautifulSoup(page.content, "html.parser")
#     # get data
#     sponsor_div = soup.find("div", {"id": "sponsor"})
#     sponsor = ""
#     if sponsor_div is not None:
#         sponsor = sponsor_div.contents[0][1:]
#
#     contact_names_tds = soup.find_all("td", {"headers" : "contactName" })
#     contact_names = ['', '']
#     if len(contact_names_tds) >= 1:
#         contact_names[0] = contact_names_tds[0].get_text().replace('Contact: ', '')
#     if len(contact_names_tds) >= 2:
#         contact_names[1] = contact_names_tds[1].get_text().replace('Contact: ', '')
#
#     contact_phones_tds = soup.find_all("td", {"headers" : "contactPhone" })
#     contact_phones = ['', '']
#     if len(contact_phones_tds) >= 1:
#         contact_phones[0] = contact_phones_tds[0].get_text()
#     if len(contact_phones_tds) >= 2:
#         contact_phones[1] = contact_phones_tds[1].get_text()
#
#     contact_emails_tds = soup.find_all("td", {"headers" : "contactEmail" })
#     contact_emails = ['', '']
#     if len(contact_phones_tds) >= 1:
#         if contact_emails_tds[0].find("a") is not None:
#             contact_emails[0] = contact_emails_tds[0].find("a").get_text()
#     if len(contact_phones_tds) >= 2:
#         if contact_emails_tds[1].find("a") is not None:
#             contact_emails[1] = contact_emails_tds[1].find("a").get_text()
#
#     conditions = ""
#     condition_header = soup.find("span", {"data-term": "Condition/disease"})
#     if condition_header is not None:
#         condition_table = condition_header.find_parent("table")
#         if condition_table is not None:
#             condition_spans = condition_table.find("td").find_all("span")
#             conditions = ",".join([s.get_text() for s in condition_spans])
#
#     # save to dict
#     study_data = StudyData(home_url+url,
#                            sponsor,
#                            contact_names[0],
#                            contact_phones[0],
#                            contact_emails[0],
#                            contact_names[1],
#                            contact_phones[1],
#                            contact_emails[1],
#                            conditions)
#     data.append(study_data)
#
# with open('data.pickle', 'wb') as handle:
#     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

"""Read Study Data from file"""
with open('20210325_data.pickle', "rb") as handle:
    data = pickle.load(handle)

"""Save information to CSV"""
email_blacklist = ['.edu',
                   '@163.com',
                   'clinical@',
                   'information@',
                   'info@',
                   'patients@',
                   'clinical.trial@',
                   'doctor@',
                   'medinfo@'
                   'clinicaltrialinfo@',
                   'clinicalresearch@',
                   'regulatory@',
                   'rehabilitation@',
                   'clinical.trials@',
                   'Clinical.Trials@'
                   'information.center@']
fieldnames = ['Sponsor',
              'Name',
              'Phone',
              'Email',
              'Name (Alt Contact)',
              'Phone (Alt Contact)',
              'Email (Alt Contact)',
              'Conditions',
              'URL']

with open('20210325_output.csv', mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for x in data:
        if valid_contact_names(x.contact_name1, x.contact_name2) and \
                valid_email(x.contact_email1, x.contact_email2, email_blacklist):
            writer.writerow({'Sponsor': x.sponsor,
                             'Name': x.contact_name1,
                             'Phone': x.contact_phone1,
                             'Email': x.contact_email1,
                             'Name (Alt Contact)': x.contact_name2,
                             'Phone (Alt Contact)': x.contact_phone2,
                             'Email (Alt Contact)': x.contact_email2,
                             'Conditions': x.conditions,
                             'URL': x.url})

"""Filter Data"""
# filter and sort here
