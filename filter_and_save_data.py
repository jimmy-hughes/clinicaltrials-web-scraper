import csv
from web_scraping_utils import *

def filter_and_save_data(data, email_blacklist, sponsor_blacklist):
    fieldnames = ['Sponsor',
                  'Name',
                  'Phone',
                  'Email',
                  'Name (Alt Contact)',
                  'Phone (Alt Contact)',
                  'Email (Alt Contact)',
                  'Conditions',
                  'URL']

    with open('output.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for x in data:
            if valid_contact_names(x.contact_name1, x.contact_name2) and \
                    valid_email(x.contact_email1, x.contact_email2, email_blacklist) and \
                    valid_sponsor(x.sponsor, sponsor_blacklist):
                writer.writerow({'Sponsor': x.sponsor,
                                 'Name': x.contact_name1,
                                 'Phone': x.contact_phone1,
                                 'Email': x.contact_email1,
                                 'Name (Alt Contact)': x.contact_name2,
                                 'Phone (Alt Contact)': x.contact_phone2,
                                 'Email (Alt Contact)': x.contact_email2,
                                 'Conditions': x.conditions,
                                 'URL': x.url})

    print("\tData successfully saved to output.csv")
