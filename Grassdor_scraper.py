from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def get_jobs(keyword, num_jobs, verbose, path):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        # Test for the "Sign Up" prompt and get rid of it.

        # try:
        #     driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  # clicking to the X.
        # except NoSuchElementException:
        #     pass
        try:
            driver.find_element(By.CLASS_NAME, "CloseButton").click()  # clicking to the X.
        except NoSuchElementException:
            pass

        # Going through each job in this page
        try:
            job_buttons = driver.find_elements(By.CSS_SELECTOR,
                                               '[class^="JobsList_jobListItem__wjTHv"]')  # Select elements with class starting with "JobsList_jobListItem"

        except NoSuchElementException:
            print("No job buttons found on the page.")
            break # jl for Job Listing. These are the buttons we're going to click.

        for job_button in job_buttons:
            time.sleep(1)

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            try:
                driver.find_element(By.CLASS_NAME, "CloseButton").click()  # clicking to the X.
            except NoSuchElementException:
                pass
            job_button.click()  # You might
            time.sleep(1)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH,
                                                       './/div[contains(@class, "JobCard_jobCardWrapper__lyvNS JobCard_selected__J9Pw8")]//span[@class="EmployerProfile_compactEmployerName__LE242"]').text

                    location = driver.find_element(By.XPATH,'.//div[contains(@class, "JobCard_jobCardWrapper__lyvNS JobCard_selected__J9Pw8")]//div[@class="JobCard_location__rCz3x"]').text
                    job_title = driver.find_element(By.XPATH,'.//div[contains(@class, "JobCard_jobCardWrapper__lyvNS JobCard_selected__J9Pw8")]//a[contains(@class, "JobCard_jobTitle___7I6y")]').text
                    job_description = driver.find_element(By.XPATH,'.//div[contains(@class, "JobCard_jobCardWrapper__lyvNS JobCard_selected__J9Pw8")]//div[@class="JobCard_jobDescriptionSnippet__yWW8q"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.XPATH,'.//div[contains(@class, "JobCard_jobCardWrapper__lyvNS JobCard_selected__J9Pw8")]//div[@class="JobCard_salaryEstimate__arV5J"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element(By.XPATH,'.//div[contains(@class, "JobCard_jobCardWrapper__lyvNS JobCard_selected__J9Pw8")]//div[@class="EmployerProfile_ratingContainer__ul0Ef"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>


            try:
                # <div class="infoEntity">
                #    <label>Headquarters</label>
                #    <span class="value">San Francisco, CA</span>
                # </div>
                headquarters = driver.find_element(By.XPATH,
                    './/div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
            except NoSuchElementException:
                headquarters = -1

            try:
                size = driver.find_element(By.XPATH,
                    './/span[text()="Size"]/following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                size = -1

            try:
                founded = driver.find_element(By.XPATH,
                    './/span[text()="Founded"]/following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                founded = -1

            try:
                type_of_ownership = driver.find_element(By.XPATH,
                    './/span[text()="Type"]/following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element(By.XPATH,
                    './/span[text()="Industry"]/following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                industry = -1

            try:
                sector = driver.find_element(By.XPATH,
                    './/span[text()="Sector"]/following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element(By.XPATH,
                    './/span[text()="Revenue"]/following-sibling::div[@class="JobDetails_overviewItemValue__xn8EF"]').text
            except NoSuchElementException:
                revenue = -1

            try:
                competitors = driver.find_element(By.XPATH,
                    './/div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
            except NoSuchElementException:
                competitors = -1
            #
            # except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
            #     headquarters = -1
            #     size = -1
            #     founded = -1
            #     type_of_ownership = -1
            #     industry = -1
            #     sector = -1
            #     revenue = -1
            #     competitors = -1

            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitors})
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH,'.//li[@class="next"]//a').click()
            print("click")
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.