import pickle
from web_scraping_utils import *
from gather_urls import gather_urls
from gather_study_data import gather_study_data
from filter_and_save_data import filter_and_save_data

def main():
    """---------------------------------"""
    """---------User Parameters---------"""
    """---------------------------------"""

    # ----- Set Stage of Script -----
    # 1: Get study URLs from search results
    # 2: Gather data from each study
    # 3: Filter and save data to CSV
    stage = 3

    # ----- stage = 1 -----
    search_range = True  # search over range of dates?
    start_date = ['03', '25', '2021']
    stop_date = ['03', '30', '2021']

    # ----- stage = 2 -----
    study_urls_file = '20210325_study_urls.pickle'

    # ----- stage = 3 -----
    study_data_file = '20210325_data.pickle'
    email_blacklist = ['.edu', '@163.com', 'clinical@', 'information@', 'info@', 'patients@', 'clinical.trial@',
                       'doctor@', 'medinfo@', 'clinicaltrialinfo@', 'clinicalresearch@', 'regulatory@',
                       'rehabilitation@', 'clinical.trials@', 'Clinical.Trials@', 'information.center@']
    sponsor_blacklist = ['University']

    """---------------------------------"""
    """---------------------------------"""
    """---------------------------------"""

    """Read Data from Skipped Stages"""
    if stage == 2:
        with open(study_urls_file, "rb") as handle:
            study_urls = pickle.load(handle)
        print("Successfully read study urls from: ", study_urls_file)
    elif stage == 3:
        with open(study_data_file, "rb") as handle:
            data = pickle.load(handle)
        print("Successfully read study data from: ", study_data_file)

    """Execute Each Stage"""
    if stage == 1:
        """Gather URLs of each study in the search results"""
        print("Stage 1:")
        if search_range:
            print("\tSearching studies updated between:", start_date, "-", stop_date)
        else:
            print("\tSearching all studies in database")
        study_urls = gather_urls(search_range, start_date, stop_date)
        stage += 1
    if stage == 2:
        """Gather Study Information"""
        print("Stage 2:")
        print("\tGathering data from each study")
        data = gather_study_data(study_urls)
        stage += 1
    if stage == 3:
        """Filter and save data to CSV"""
        print("Stage 3:")
        print("\tFiltering data and saving to CSV")
        filter_and_save_data(data, email_blacklist, sponsor_blacklist)


if __name__ == "__main__":
    main()
