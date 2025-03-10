import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import os

# Base URL for Infosys careers
BASE_URL = "https://career.infosys.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_last_page_infosys(page_html):
    """
    Extract the last page number from the pagination element.
    Assumes there is a "Last" link with a page number.
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

def scrape_infosys_job_cards(page_html):
    """
    Parse the Infosys job card listings from the page HTML.
    """
    soup = BeautifulSoup(page_html, "html.parser")
    # Each job card container
    cards = soup.select("div.customCard.ng-star-inserted")
    print("Job card**********", cards)
    jobs = []
    for card in cards:
        # Job Title
        title_elem = card.select_one("span[name='PostingTitle']")
        title = title_elem.get_text(strip=True) if title_elem else None

        # Company (should be Infosys Limited)
        company_elem = card.select_one("span[name='iconcompany']")
        company = company_elem.get_text(strip=True) if company_elem else None

        # Location
        loc_elem = card.select_one("span[name='titleLoc']")
        location = loc_elem.get_text(strip=True) if loc_elem else None

        # Skills: find the span following the "Skills:" label
        skills = ""
        skills_label = card.find("span", text="Skills:")
        if skills_label:
            skills_elem = skills_label.find_next_sibling("span", class_="secondaryText")
            if skills_elem:
                skills = skills_elem.get_text(strip=True)

        # Responsibilities: from the span with name "jobRoles"
        resp_elem = card.select_one("span[name='jobRoles']")
        responsibilities = resp_elem.get_text(strip=True) if resp_elem else ""

        # For now, the apply link is not extracted (set to None)
        apply_link = None

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "skills": skills,
            "responsibilities": responsibilities,
            "apply_link": apply_link
        })
    return jobs

def main():
    csv_file = "infosys_jobs.csv"
    # Load existing jobs if CSV exists; use job title + location as unique identifier.
    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file)
        existing_ids = set(df_existing.apply(lambda row: f"{row['title']}|{row['location']}", axis=1))
        aggregated_jobs = df_existing.to_dict("records")
    else:
        existing_ids = set()
        aggregated_jobs = []

    # Start by fetching page 1 to determine the total pages.
    search_url_page1 = urljoin(BASE_URL, "/joblist")
    try:
        
        response = requests.get(search_url_page1, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print("Error fetching page 1:", e)
        return

    last_page = get_last_page_infosys(response.text)
    print(f"Total pages found: {last_page}")

    new_jobs_count = 0
    # Iterate through pages
    for page in range(1, last_page + 1):
        page_url = urljoin(BASE_URL, f"/joblist?page={page}")
        print(f"Scraping Infosys page {page}: {page_url}")
        try:
            response = requests.get(page_url, headers=HEADERS)
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            continue

        jobs_on_page = scrape_infosys_job_cards(response.text)
        print("**************", jobs_on_page)
        new_jobs = []
        for job in jobs_on_page:
            # Unique identifier: title + location
            unique_id = f"{job['title']}|{job['location']}"
            if unique_id not in existing_ids:
                new_jobs.append(job)
                existing_ids.add(unique_id)

        if not new_jobs:
            print("No new jobs found on this page. Stopping further scraping.")
            break

        aggregated_jobs.extend(new_jobs)
        new_jobs_count += len(new_jobs)

    # Save aggregated data to CSV
    df = pd.DataFrame(aggregated_jobs)
    df.to_csv(csv_file, index=False)
    print(f"Scraping complete. {new_jobs_count} new jobs added. Data saved to {csv_file}")

if __name__ == "__main__":
    main()
