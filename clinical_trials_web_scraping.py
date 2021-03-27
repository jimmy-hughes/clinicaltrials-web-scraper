import requests
import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pickle
import csv

"""Classes"""
class StudyData:
    def __init__(self, url, sponsor, contact_name1, contact_phone1, contact_email1, contact_name2, contact_phone2,
                 contact_email2, conditions):
        self.url = url
        self.sponsor = sponsor
        self.contact_name1 = contact_name1
        self.contact_phone1 = contact_phone1
        self.contact_email1 = contact_email1
        self.contact_name2 = contact_name2
        self.contact_phone2 = contact_phone2
        self.contact_email2 = contact_email2
        self.conditions = conditions

"""Functions"""
def get_urls(page, urls):
    # get table rows from results table
    table_rows = page.find_all(name="tr", class_=["odd parent", "even parent"])

    # loop over rows and save hyperlinks
    for row in table_rows:
        urls.append(row.find(name="a", href=True)['href'])

    return urls

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
with open('20210325_study_urls.pickle', "rb") as handle:
    study_urls = pickle.load(handle)

"""Gather Study Information"""
home_url = 'https://clinicaltrials.gov'
data = []
# for url in study_urls:
for i in range(5000,10000):
    url = study_urls[i]
    # open webpage
    page = requests.get(home_url+url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    # get data
    sponsor_div = soup.find("div", {"id": "sponsor"})
    sponsor = ""
    if sponsor_div is not None:
        sponsor = sponsor_div.contents[0][1:]

    contact_names_tds = soup.find_all("td", {"headers" : "contactName" })
    contact_names = ['', '']
    if len(contact_names_tds) >= 1:
        contact_names[0] = contact_names_tds[0].get_text().replace('Contact: ', '')
    if len(contact_names_tds) >= 2:
        contact_names[1] = contact_names_tds[1].get_text().replace('Contact: ', '')

    contact_phones_tds = soup.find_all("td", {"headers" : "contactPhone" })
    contact_phones = ['', '']
    if len(contact_phones_tds) >= 1:
        contact_phones[0] = contact_phones_tds[0].get_text()
    if len(contact_phones_tds) >= 2:
        contact_phones[1] = contact_phones_tds[1].get_text()

    contact_emails_tds = soup.find_all("td", {"headers" : "contactEmail" })
    contact_emails = ['', '']
    if len(contact_phones_tds) >= 1:
        if contact_emails_tds[0].find("a") is not None:
            contact_emails[0] = contact_emails_tds[0].find("a").get_text()
    if len(contact_phones_tds) >= 2:
        if contact_emails_tds[1].find("a") is not None:
            contact_emails[1] = contact_emails_tds[1].find("a").get_text()

    conditions = ""
    condition_table = soup.find("span", {"data-term": "Condition/disease"}).find_parent("table")
    if condition_table is not None:
        condition_spans = condition_table.find("td").find_all("span")
        conditions = ",".join([s.get_text() for s in condition_spans])

    # save to dict
    study_data = StudyData(home_url+url,
                           sponsor,
                           contact_names[0],
                           contact_phones[0],
                           contact_emails[0],
                           contact_names[1],
                           contact_phones[1],
                           contact_emails[1],
                           conditions)
    data.append(study_data)

with open('data_5000-10000.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# """Save information to CSV"""
# with open('output.csv', mode='w') as csv_file:
#     fieldnames = ['sponsor',
#                   'conditions',
#                   'contact_name_1',
#                   'contact_phone_1',
#                   'contact_email_1',
#                   'contact_name_2',
#                   'contact_phone_2',
#                   'contact_email_2',
#                   'url']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()
#     for x in data:
#         writer.writerow({'sponsor': x.sponsor,
#                          'conditions': x.conditions,
#                          'contact_name_1': x.contact_name1,
#                          'contact_phone_1': x.contact_phone1,
#                          'contact_email_1': x.contact_email1,
#                          'contact_name_2': x.contact_name2,
#                          'contact_phone_2': x.contact_phone2,
#                          'contact_email_2': x.contact_email2,
#                          'url': home_url+x.url})

"""Filter Data"""
# filter and sort here
