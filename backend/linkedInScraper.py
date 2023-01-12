# Web Scraping Application that gets information from LinkedIn, Indeed, Google Jobs and Monster

    # Pull links from linkedIn and send to discord bot that will display
    # Discord bot will only output the diff of the previous message
    # Repeat for indeed, monster and google jobs

    # Begin working on some sort of api endpoint that we can access from react
    # Will have search in react to search for job types and will display all jobs 
    # Need configurable searching in web scraper

    # different classes for each scraper
    # create a main driver that creates a scraper and return data
    # filter by number of days relevance etc

import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

class linkedInScraper:
    def __init__(self, job_query, number_of_entries):
        # self.location = location
        self.job_query = job_query
        self.number_of_entries = number_of_entries
        self.url = self.generate_url()
        self.job_counter = 0
        self.json_object = []

    def get_all_linkedin_links(self):
        self.linkedin_scrape(self.url, 0)
        return self.json_object
                
    def linkedin_scrape(self, webpage, page_num):
        global count
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        next_page = webpage + str(page_num)
        response = requests.get(str(next_page))

        jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')

        for job in jobs:
            # Grab all relevant information from job listing
            job_title = job.find('h3', class_= 'base-search-card__title').text.strip()
            job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
            job_location = job.find('span', class_="job-search-card__location").text.strip()
            job_link = job.find('a', class_= 'base-card__full-link')['href']

            # Add to JSON object
            item = {
                'ID' : self.job_counter,
                'Source' : 'LinkedIn',
                'Title': job_title, 
                'Company': job_company, 
                'Location': job_location, 
                'Link': job_link}
            self.job_counter+=1
            
            self.json_object.append(item)

            if self.job_counter >= self.number_of_entries:
                self.quit_out()
                return

        if page_num < 25 + self.number_of_entries:
            page_num = page_num + 25
            self.linkedin_scrape(self.url, page_num)
        else:
           self.quit_out()

    def quit_out(self):
        # print(self.json_object)
        with open ("data/jobs.json", "w",encoding='utf-8') as outfile:
            json.dump(self.json_object, outfile, indent=4)

        outfile.close()

    def generate_url(self):
        replaced_job_title = self.job_query.replace(" ", "%20")
        url ="https://www.linkedin.com/jobs/search?keywords=" + replaced_job_title + "&location=Arcadia%2C%20California%2C%20United%20States&geoId=107117755&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
        return url
    
# linkedInScraper("Entry Level Civil Engineer", 100).get_all_linkedin_links()
