# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from urllib.parse import urljoin

# # Base URL for Cognizant careers (adjust if needed)
# BASE_URL = "https://careers.cognizant.com"

# # Common headers for HTTP requests
# HEADERS = {"User-Agent": "Mozilla/5.0"}

# def scrape_job_cards(page_html):
#     """
#     Parse the job card listings from the page HTML.
#     """
#     soup = BeautifulSoup(page_html, "html.parser")
#     # Each job card container
#     cards = soup.select("div.card.card-job")
#     jobs = []
    
#     for card in cards:
#         # Extract job title and relative link
#         a_tag = card.select_one("h2.card-title a.stretched-link.js-view-job")
#         if a_tag:
#             title = a_tag.get_text(strip=True)
#             relative_link = a_tag["href"]
#             # Build the absolute URL for the job detail page
#             link = urljoin(BASE_URL, relative_link)
#         else:
#             title, link = None, None
        
#         # Extract location from the first list item in the job meta list
#         location = None
#         meta_items = card.select("ul.list-inline.job-meta li")
#         if meta_items:
#             location = meta_items[0].get_text(strip=True)
        
#         jobs.append({
#             "title": title,
#             "link": link,
#             "location": location
#         })
#     return jobs

# def scrape_job_detail(url):
#     """
#     Fetch the job detail page and extract the detailed description and key job meta details.
#     """
#     response = requests.get(url, headers=HEADERS)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, "html.parser")
    
#     # Extract the job description from the article content
#     article = soup.select_one("div.col-lg-8.main-col article.cms-content")
#     description = article.get_text(separator="\n", strip=True) if article else ""
    
#     # Extract key details (e.g., job number, travel required, etc.) from the <dl class="job-meta">
#     key_details = {}
#     for dt in soup.select("aside.col-lg-4.sidebar dl.job-meta dt"):
#         dd = dt.find_next_sibling("dd")
#         if dd:
#             key = dt.get_text(strip=True).replace(":", "")
#             value = dd.get_text(strip=True)
#             key_details[key] = value
    
#     return description, key_details

# def main():
#     # For demonstration purposes, we use a sample job search URL.
#     # Replace this with the actual URL that lists Cognizant job cards.
#     search_url = urljoin(BASE_URL, "/global-en/jobs/")
    
#     try:
#         response = requests.get(search_url, headers=HEADERS)
#         response.raise_for_status()
#     except Exception as e:
#         print(f"Error fetching job list page: {e}")
#         return
    
#     # Scrape the job cards from the search results page
#     jobs = scrape_job_cards(response.text)
    
#     # For each job, fetch the detailed job description and key details.
#     for job in jobs:
#         if job["link"]:
#             try:
#                 description, key_details = scrape_job_detail(job["link"])
#                 job["description"] = description
#                 job["key_details"] = key_details
#             except Exception as e:
#                 print(f"Failed to scrape details for {job['link']}: {e}")
#                 job["description"] = ""
#                 job["key_details"] = {}
    
#     # Save the aggregated data to a CSV file
#     df = pd.DataFrame(jobs)
#     df.to_csv("cognizant_jobs.csv", index=False)
#     print("Scraping complete. Data saved to cognizant_jobs.csv")

# if __name__ == "__main__":
#     main()


import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import os

# Base URL for Cognizant careers (adjust if needed)
BASE_URL = "https://careers.cognizant.com"
# Common headers for HTTP requests
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_last_page(page_html):
    """
    Parse the last page number from the first page HTML.
    """
    soup = BeautifulSoup(page_html, "html.parser")
    last_page_elem = soup.select_one("li.page-item a[rel*='last']")
    if last_page_elem:
        try:
            last_page = int(last_page_elem.get_text(strip=True))
            return last_page
        except Exception as e:
            print("Error parsing last page number:", e)
    return 1

def scrape_job_cards(page_html):
    """
    Parse the job card listings from the page HTML.
    """
    soup = BeautifulSoup(page_html, "html.parser")
    # Each job card container
    cards = soup.select("div.card.card-job")
    jobs = []
    
    for card in cards:
        # Extract job title and relative link
        a_tag = card.select_one("h2.card-title a.stretched-link.js-view-job")
        if a_tag:
            title = a_tag.get_text(strip=True)
            relative_link = a_tag["href"]
            # Build the absolute URL for the job detail page
            link = urljoin(BASE_URL, relative_link)
        else:
            title, link = None, None
        
        # Extract location from the first list item in the job meta list
        location = None
        meta_items = card.select("ul.list-inline.job-meta li")
        if meta_items:
            location = meta_items[0].get_text(strip=True)
        
        jobs.append({
            "title": title,
            "link": link,
            "location": location
        })
    return jobs

def scrape_job_detail(url):
    """
    Fetch the job detail page and extract the detailed description and key job meta details.
    """
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract the job description from the article content
    article = soup.select_one("div.col-lg-8.main-col article.cms-content")
    description = article.get_text(separator="\n", strip=True) if article else ""
    
    # Extract key details (e.g., job number, travel required, etc.) from the <dl class="job-meta">
    key_details = {}
    for dt in soup.select("aside.col-lg-4.sidebar dl.job-meta dt"):
        dd = dt.find_next_sibling("dd")
        if dd:
            key = dt.get_text(strip=True).replace(":", "")
            value = dd.get_text(strip=True)
            key_details[key] = value
    
    return description, key_details

def main():
    csv_file = "cognizant_jobs.csv"
    # Load existing jobs if CSV exists; use job link as unique identifier.
    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file)
        existing_links = set(df_existing["link"].tolist())
        aggregated_jobs = df_existing.to_dict("records")
    else:
        existing_links = set()
        aggregated_jobs = []
    
    # Start by fetching page 1 to determine the last page number.
    search_url_page1 = urljoin(BASE_URL, "/global-en/jobs/?page=1")
    try:
        response = requests.get(search_url_page1, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print("Error fetching page 1:", e)
        return
    
    last_page = get_last_page(response.text)
    print(f"Total pages found: {last_page}")
    
    new_jobs_count = 0
    # Loop through pages
    for page in range(1, last_page + 1):
        page_url = urljoin(BASE_URL, f"/global-en/jobs/?page={page}")
        print(f"Scraping page {page}: {page_url}")
        try:
            response = requests.get(page_url, headers=HEADERS)
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            continue
        
        jobs_on_page = scrape_job_cards(response.text)
        # Filter out jobs that already exist
        new_jobs = [job for job in jobs_on_page if job["link"] not in existing_links]
        
        if not new_jobs:
            print("No new jobs found on this page. Stopping further scraping.")
            break
        
        for job in new_jobs:
            try:
                description, key_details = scrape_job_detail(job["link"])
                job["description"] = description
                job["key_details"] = key_details
                aggregated_jobs.append(job)
                existing_links.add(job["link"])
                new_jobs_count += 1
            except Exception as e:
                print(f"Failed to scrape details for {job['link']}: {e}")
    
    # Save the aggregated data to CSV (overwriting the old file)
    df = pd.DataFrame(aggregated_jobs)
    df.to_csv(csv_file, index=False)
    print(f"Scraping complete. {new_jobs_count} new jobs added. Data saved to {csv_file}")

if __name__ == "__main__":
    main()
    
    # https://career.infosys.com/jobs/jobsStatus
