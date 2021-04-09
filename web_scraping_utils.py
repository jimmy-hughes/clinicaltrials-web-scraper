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


def get_urls_from_page(page, urls):
    # get table rows from results table
    table_rows = page.find_all(name="tr", class_=["odd parent", "even parent"])

    # loop over rows and save hyperlinks
    for row in table_rows:
        urls.append(row.find(name="a", href=True)['href'])

    return urls


def valid_email(email1, email2, blacklist):
    for x in blacklist:
        if x in email1 and (x in email2 or email2 == ''):
            return False
    return True

def valid_sponsor(sponsor, blacklist):
    for x in blacklist:
        if x in sponsor:
            return False
    return True


def valid_contact_names(name1 , name2):
    if name1 == '' and name2 == '':
        return False
    else:
        return True
