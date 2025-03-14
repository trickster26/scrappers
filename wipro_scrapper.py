# import requests
# from bs4 import BeautifulSoup
# import time
# import json
# from tqdm import tqdm
# import re

# class WiproJobScraper:
#     def __init__(self):
#         self.base_url = "https://careers.wipro.com/search"
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
#         }
#         self.jobs = []

#     def get_total_pages(self, soup):
#         """Get total number of pages from pagination"""
#         pagination = soup.find('div', class_='pagination-well')
#         if pagination:
#             total_text = pagination.find('span', class_='paginationLabel')
#             if total_text:
#                 total_jobs = int(total_text.find_all('b')[-1].text)
#                 return (total_jobs // 25) + 1  # 25 jobs per page
#         return 1

#     def scrape_job_listings(self, page_num=0):
#         """Scrape job listings from a specific page"""
#         params = {
#             'q': '',
#             'sortColumn': 'referencedate',
#             'sortDirection': 'desc',
#             'startrow': page_num * 25
#         }
        
#         try:
#             response = requests.get(self.base_url, headers=self.headers, params=params)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             job_rows = soup.find_all('tr', class_='data-row')
            
#             for row in job_rows:
#                 job = {}
#                 title_elem = row.find('a', class_='jobTitle-link')
#                 if title_elem:
#                     job['title'] = title_elem.text.strip()
#                     job['link'] = "https://careers.wipro.com" + title_elem['href']
                
#                 location_elem = row.find('span', class_='jobLocation')
#                 if location_elem:
#                     job['location'] = location_elem.text.strip()
                
#                 date_elem = row.find('span', class_='jobDate')
#                 if date_elem:
#                     job['date'] = date_elem.text.strip()
                
#                 job_details = self.scrape_job_details(job['link'])
#                 job.update(job_details)
                
#                 self.jobs.append(job)
            
#             return True
            
#         except requests.RequestException as e:
#             print(f"Error scraping page {page_num}: {e}")
#             return False

#     def scrape_job_details(self, job_url):
#         """Scrape detailed information from job description page"""
#         details = {}
#         try:
#             response = requests.get(job_url, headers=self.headers)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             title_elem = soup.find('span', {'data-careersite-propertyid': 'title'})
#             if title_elem:
#                 details['title'] = title_elem.text.strip()
            
#             req_id_elem = soup.find('span', {'data-careersite-propertyid': 'customfield1'})
#             if req_id_elem:
#                 details['requisition_id'] = req_id_elem.text.strip()
            
#             city_elem = soup.find('span', {'data-careersite-propertyid': 'city'})
#             if city_elem:
#                 details['city'] = city_elem.text.strip()
            
#             country_elem = soup.find('span', {'data-careersite-propertyid': 'country'})
#             if country_elem:
#                 details['country'] = country_elem.text.strip()
            
#             desc_elem = soup.find('span', {'data-careersite-propertyid': 'description'})
#             if desc_elem:
#                 details['description'] = desc_elem.text.strip()
                
#                 salary_pattern = r'Expected annual pay for this role ranges from \$([\d,]+) to \$([\d,]+)'
#                 salary_match = re.search(salary_pattern, details['description'])
#                 if salary_match:
#                     details['salary_range'] = {
#                         'min': salary_match.group(1).replace(',', ''),
#                         'max': salary_match.group(2).replace(',', '')
#                     }
            
#             apply_button = soup.find('button', text='Apply now')
#             if apply_button and apply_button.get('href'):
#                 details['apply_link'] = "https://careers.wipro.com" + apply_button['href']
            
#             return details
            
#         except requests.RequestException as e:
#             print(f"Error scraping job details from {job_url}: {e}")
#             return details

#     def scrape_all_jobs(self, max_pages=None):
#         """Scrape all jobs across all pages"""
#         response = requests.get(self.base_url, headers=self.headers, params={
#             'q': '',
#             'sortColumn': 'referencedate',
#             'sortDirection': 'desc'
#         })
#         soup = BeautifulSoup(response.text, 'html.parser')
#         total_pages = self.get_total_pages(soup)
        
#         if max_pages:
#             total_pages = min(max_pages, total_pages)
        
#         print(f"Total pages to scrape: {total_pages}")
        
#         for page in tqdm(range(total_pages)):
#             success = self.scrape_job_listings(page)
#             if not success:
#                 print(f"Stopping at page {page} due to error")
#                 break
#             self.save_to_json()  # Save after each page
#             time.sleep(2)

#     def save_to_json(self, filename='wipro_jobs.json'):
#         """Save scraped jobs to JSON file"""
#         try:
#             # Write the jobs list to JSON file
#             with open(filename, 'w', encoding='utf-8') as f:
#                 json.dump(self.jobs, f, indent=2, ensure_ascii=False)
#             print(f"Saved {len(self.jobs)} jobs to {filename}")
#         except Exception as e:
#             print(f"Error saving to JSON: {e}")

# def main():
#     scraper = WiproJobScraper()
#     # Scrape all jobs (or set max_pages for testing, e.g., max_pages=2)
#     scraper.scrape_all_jobs(max_pages=2)  # Limiting to 2 pages for demonstration
#     # Final save (optional since we save after each page)
#     scraper.save_to_json()

# if __name__ == "__main__":
#     main()

import requests
from bs4 import BeautifulSoup
import time
import json
from tqdm import tqdm
import re

class WiproJobScraper:
    def __init__(self):
        self.base_url = "https://careers.wipro.com/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.jobs = []

    def get_total_pages(self, soup):
        """Get total number of pages from pagination"""
        pagination = soup.find('div', class_='pagination-well')
        if pagination:
            total_text = pagination.find('span', class_='paginationLabel')
            if total_text:
                total_jobs = int(total_text.find_all('b')[-1].text)
                return (total_jobs // 25) + 1  # 25 jobs per page
        return 1

    def scrape_job_listings(self, page_num=0):
        """Scrape job listings from a specific page"""
        params = {
            'q': '',
            'sortColumn': 'referencedate',
            'sortDirection': 'desc',
            'startrow': page_num * 25
        }
        
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_rows = soup.find_all('tr', class_='data-row')
            
            for row in job_rows:
                job = {}
                title_elem = row.find('a', class_='jobTitle-link')
                if title_elem:
                    job['title'] = title_elem.text.strip()
                    job['link'] = "https://careers.wipro.com" + title_elem['href']
                
                location_elem = row.find('span', class_='jobLocation')
                if location_elem:
                    job['location'] = location_elem.text.strip()
                
                date_elem = row.find('span', class_='jobDate')
                if date_elem:
                    job['date'] = date_elem.text.strip()
                
                job_details = self.scrape_job_details(job['link'])
                job.update(job_details)
                
                self.jobs.append(job)
            
            return True
            
        except requests.RequestException as e:
            print(f"Error scraping page {page_num}: {e}")
            return False

    def scrape_job_details(self, job_url):
        """Scrape detailed information from job description page"""
        details = {}
        try:
            response = requests.get(job_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title_elem = soup.find('span', {'data-careersite-propertyid': 'title'})
            if title_elem:
                details['title'] = title_elem.text.strip()
            
            req_id_elem = soup.find('span', {'data-careersite-propertyid': 'customfield1'})
            if req_id_elem:
                details['requisition_id'] = req_id_elem.text.strip()
            
            city_elem = soup.find('span', {'data-careersite-propertyid': 'city'})
            if city_elem:
                details['city'] = city_elem.text.strip()
            
            country_elem = soup.find('span', {'data-careersite-propertyid': 'country'})
            if country_elem:
                details['country'] = country_elem.text.strip()
            
            desc_elem = soup.find('span', {'data-careersite-propertyid': 'description'})
            if desc_elem:
                details['description'] = desc_elem.text.strip()
                
                salary_pattern = r'Expected annual pay for this role ranges from \$([\d,]+) to \$([\d,]+)'
                salary_match = re.search(salary_pattern, details['description'])
                if salary_match:
                    details['salary_range'] = {
                        'min': salary_match.group(1).replace(',', ''),
                        'max': salary_match.group(2).replace(',', '')
                    }
            
            apply_button = soup.find('button', text='Apply now')
            if apply_button and apply_button.get('href'):
                details['apply_link'] = "https://careers.wipro.com" + apply_button['href']
            
            return details
            
        except requests.RequestException as e:
            print(f"Error scraping job details from {job_url}: {e}")
            return details

    def scrape_all_jobs(self):
        """Scrape all jobs across all pages until the last page"""
        response = requests.get(self.base_url, headers=self.headers, params={
            'q': '',
            'sortColumn': 'referencedate',
            'sortDirection': 'desc'
        })
        soup = BeautifulSoup(response.text, 'html.parser')
        total_pages = self.get_total_pages(soup)
        
        print(f"Total pages to scrape: {total_pages}")
        
        for page in tqdm(range(total_pages)):
            success = self.scrape_job_listings(page)
            if not success:
                print(f"Stopping at page {page} due to error")
                break
            self.save_to_json()  # Save after each page
            time.sleep(2)  # Delay to be respectful to the server

    def save_to_json(self, filename='wipro_jobs.json'):
        """Save scraped jobs to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jobs, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self.jobs)} jobs to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")

def main():
    scraper = WiproJobScraper()
    scraper.scrape_all_jobs()
    scraper.save_to_json()  # Final save

if __name__ == "__main__":
    main()