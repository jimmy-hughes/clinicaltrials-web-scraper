import requests
import bs4
import pickle
from web_scraping_utils import *

def gather_study_data(study_urls):
    home_url = 'https://clinicaltrials.gov'
    data = []
    for url in study_urls:
        # open webpage
        page = requests.get(home_url + url)
        soup = bs4.BeautifulSoup(page.content, "html.parser")
        # get data
        sponsor_div = soup.find("div", {"id": "sponsor"})
        sponsor = ""
        if sponsor_div is not None:
            sponsor = sponsor_div.contents[0][1:]

        contact_names_tds = soup.find_all("td", {"headers": "contactName"})
        contact_names = ['', '']
        if len(contact_names_tds) >= 1:
            contact_names[0] = contact_names_tds[0].get_text().replace('Contact: ', '')
        if len(contact_names_tds) >= 2:
            contact_names[1] = contact_names_tds[1].get_text().replace('Contact: ', '')

        contact_phones_tds = soup.find_all("td", {"headers": "contactPhone"})
        contact_phones = ['', '']
        if len(contact_phones_tds) >= 1:
            contact_phones[0] = contact_phones_tds[0].get_text()
        if len(contact_phones_tds) >= 2:
            contact_phones[1] = contact_phones_tds[1].get_text()

        contact_emails_tds = soup.find_all("td", {"headers": "contactEmail"})
        contact_emails = ['', '']
        if len(contact_phones_tds) >= 1:
            if contact_emails_tds[0].find("a") is not None:
                contact_emails[0] = contact_emails_tds[0].find("a").get_text()
        if len(contact_phones_tds) >= 2:
            if contact_emails_tds[1].find("a") is not None:
                contact_emails[1] = contact_emails_tds[1].find("a").get_text()

        conditions = ""
        condition_header = soup.find("span", {"data-term": "Condition/disease"})
        if condition_header is not None:
            condition_table = condition_header.find_parent("table")
            if condition_table is not None:
                condition_spans = condition_table.find("td").find_all("span")
                conditions = ",".join([s.get_text() for s in condition_spans])

        # save to dict
        study_data = StudyData(home_url + url,
                               sponsor,
                               contact_names[0],
                               contact_phones[0],
                               contact_emails[0],
                               contact_names[1],
                               contact_phones[1],
                               contact_emails[1],
                               conditions)
        data.append(study_data)

    with open('data.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("\tData successfully saved to data.pickle")

    return data